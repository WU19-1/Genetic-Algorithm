from typing import Dict
from models.genetic_algorithm.configuration import Configuration
from models.genetic_algorithm.trait import Trait
from handlers.input_handler import input_message
from controller.stress_test_controller import build_images, build_single_image, build_website, build_stress_test, run_single_website, run_websites, run_container
from random import choices, randint, random
from os import getenv, getcwd

MAX_CONFIGURATION = 0
MAX_TRAIT = 0
MAX_GENERATION = 0
RESPONSE_TIME_GOAL = 0

WEB_CONTAINERS = [
    {
        "container_name" : "cweb1",
        "name" : "web1", 
        "port" : "5000:80",
        "version" : "latest",
        "path" : "%s"%(getcwd().replace('\\', '/') + "/container/web1/"),
        "arg" : {},
        "volume": None,
        "is_detach": True,
        "max_cpu_count" : 2,
        "max_cpu_percentage" : 100,
        "min_ram" : 1024,
        "max_ram" : 2048,
    },
    {
        "container_name" : "cweb2",
        "name" : "web2",
        "port" : "5001:80",
        "version" : "latest",
        "path" : "%s"%(getcwd().replace('\\', '/') + "/container/web2/"),
        "arg" : {},
        "volume": None,
        "is_detach": True,
        "max_cpu_count" : 2,
        "max_cpu_percentage" : 100,
        "min_ram" : 2048,
        "max_ram" : 4096,
    },
    {
        "container_name" : "cweb3",
        "name" : "web3",
        "port" : "5002:80",
        "version" : "latest",
        "path" : "%s"%(getcwd().replace('\\', '/') + "/container/web3/"),
        "arg" : {},
        "volume": None,
        "is_detach": True,
        "max_cpu_count" : 2,
        "max_cpu_percentage" : 75,
        "min_ram" : 2048,
        "max_ram" : 3072,
    }
]

def generate_configuration():
    configurations = []
    for _ in range(MAX_CONFIGURATION):
        configuration = Configuration()
        configurations.append(configuration)
    return configurations

def generate_configuration_modified(web_config : dict):
    configurations = []
    for _ in range(MAX_CONFIGURATION):
        configuration = Configuration({
            "max_cpu_count" : web_config["max_cpu_count"],
            "max_cpu_percentage" : web_config["max_cpu_percentage"],
            "min_ram" : web_config["min_ram"],
            "max_ram" : web_config["max_ram"]
        })
        configurations.append(configuration)
    return configurations

def generate_traits():
    traits = []
    trait_object = {"total_trait": MAX_CONFIGURATION, "trait": None}
    for _ in range(MAX_TRAIT):
        trait = Trait(trait_object)
        traits.append(trait)
    return traits


def calculate_configuration(trait: Trait, configurations: [Configuration]):
    trait.reset_configuration()
    for i in range(MAX_CONFIGURATION):
        if trait.trait[i] == 1:
            trait.cpu_count.append(configurations[i].cpu_count)
            trait.cpu_percent.append(configurations[i].cpu_percent)
            trait.memory_limit.append(configurations[i].memory_limit)


def fitness_function(trait: Trait, configurations: [Configuration], web : Dict):
    if 1 not in trait.trait:
        return 0

    calculate_configuration(trait, configurations)

    cpu_count, cpu_percent, memory_limit = trait.get_average_configuration()
    print("CPU({} core & {}%), MEM({} MB) => ".format(cpu_count, cpu_percent, memory_limit[:-1]), end="")

    average = run_single_website(cpu_count, cpu_percent, memory_limit, web)
    return average


def crossover(first_trait: Trait, second_trait: Trait):
    if MAX_CONFIGURATION >= 2:
        recombination_index = randint(0, MAX_CONFIGURATION - 1)

        first_trait_temp = first_trait.trait
        second_trait_temp = second_trait.trait

        first_trait.trait = first_trait_temp[0: recombination_index] + second_trait_temp[recombination_index:]
        second_trait.trait = second_trait_temp[0: recombination_index] + first_trait_temp[recombination_index:]

    return first_trait, second_trait


def mutation(trait: Trait, probability: float = 0.2):
    for index in range(MAX_CONFIGURATION):
        mutation_chance = random()
        if mutation_chance < probability:
            trait.trait[index] = abs(trait.trait[index] - 1)

    return trait


def calculate_response_time(traits: [Trait], configurations: [Configuration], web : Dict):
    for index_trait, trait in enumerate(traits):
        print("    [^] Index-{} => ".format(index_trait), end="")
        trait.average_response_time = fitness_function(trait, configurations, web)
        print("{} ms".format(trait.average_response_time))

    return traits


def create_new_traits(traits: [Trait], configurations: [Configuration]):
    new_generation = []
    weights = []

    for trait in traits:
        weights.append(2000 - trait.average_response_time)

    for _ in range(MAX_TRAIT // 2):
        chosen_trait = choices(traits, k=2, weights=weights)

        first_new_trait = Trait({"total_trait": chosen_trait[0].total_trait, "trait": chosen_trait[0].trait})
        second_new_trait = Trait({"total_trait": chosen_trait[1].total_trait, "trait": chosen_trait[1].trait})

        first_new_trait, second_new_trait = crossover(first_new_trait, second_new_trait)
        first_new_trait = mutation(first_new_trait)
        second_new_trait = mutation(second_new_trait)
        calculate_configuration(first_new_trait, configurations)
        calculate_configuration(second_new_trait, configurations)

        new_generation.append(first_new_trait)
        new_generation.append(second_new_trait)

    return new_generation


def show_result(trait: Trait):
    cpu_count, cpu_percent, memory_limit = trait.get_average_configuration()

    input_message(withInput=False)
    print("[*] Best Configuration")
    print("[*] CPU Count     : {} core".format(cpu_count))
    print("[*] CPU Percent   : {}%".format(cpu_percent))
    print("[*] Memory Limit  : {} MB".format(memory_limit[:-1]))
    print("[*] Response Time : {} ms".format(trait.average_response_time))

def genetic_algorithm():
    global MAX_CONFIGURATION, MAX_TRAIT, MAX_GENERATION, RESPONSE_TIME_GOAL

    for web in WEB_CONTAINERS:

        MAX_CONFIGURATION = int(getenv("MAX_CONFIGURATION"))
        MAX_TRAIT = int(getenv("MAX_TRAIT"))
        MAX_GENERATION = int(getenv("MAX_GENERATION"))
        RESPONSE_TIME_GOAL = int(getenv("RESPONSE_TIME_GOAL"))

        print("[*] Building website images.")
        build_single_image(web_container=web)

        # print("[*] Building stress test image.")
        # build_stress_test(getenv("PYTHON_IMAGE_TOTAL_REQUEST"), getenv("PYTHON_IMAGE_TOTAL_CONNECTION"))

        print("[*] Generating configurations and traits.")
        configurations = generate_configuration_modified(web)
        traits = generate_traits()

        print("[*] Calculating response time for each traits.")
        traits = calculate_response_time(traits, configurations, web)

        print("[*] Starting genetic algorithm.", end="\n\n")

        index_generation = 0
        for i in range(1, MAX_GENERATION + 1):
            print("[*] Generation {}.".format(str(i)))

            print("[*] Creating new traits.")
            traits = create_new_traits(traits, configurations)

            print("[*] Calculating response time for each new traits.")
            traits = calculate_response_time(traits, configurations, web)

            print("[*] Sorting all traits.")
            traits = sorted(traits, key=lambda t: t.average_response_time)

            for index_trait, trait in enumerate(traits):
                cpu_count, cpu_percent, memory_limit = trait.get_average_configuration()
                print("    [^] Index-{} => CPU({} core & {}%), MEM({} MB) => {} ms"
                    .format(index_trait, cpu_count, cpu_percent, memory_limit[:-1], trait.average_response_time))

            if traits[0].average_response_time <= RESPONSE_TIME_GOAL and traits[0].average_response_time != 0:
                index_generation = i
                break

            print("[*] End of generation {}".format(str(i)), end="\n\n")

        print("[*] The genetic algorithm has been completed in the generation {}.".format(index_generation))

        choose = 1
        for i,t in enumerate(traits):
            cpu_count, cpu_percent, memory_limit = t.get_average_configuration()
            print("{} => CPU({} core & {}%), MEM({} MB) => {} ms".format((i + 1), cpu_count, cpu_percent, memory_limit[:-1], t.average_response_time))
        while True:
            choose = int(input("Choose configuration for %s [ 1 - %d ] : "%(web["name"],len(traits))))
            if choose >= 1 and choose <= len(traits):
                break
        chosen_trait = traits.pop(choose - 1).get_average_configuration()
        print("[*] Running %s container with chosen configuration..."%(web["name"]))
        print(chosen_trait)
        run_container(web, {
            'cpu_count' : chosen_trait[0],
            'cpu_percent' : chosen_trait[1],
            'memory_limit' : chosen_trait[2],
            'memory_swap_limit' : chosen_trait[2],
        })

        

