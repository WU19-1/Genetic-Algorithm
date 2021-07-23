from random import choices, paretovariate
from models import Configuration
from models import Population
from stress_test import stress_test
from os import getcwd
from docker_controller import create_container, create_image, stop_container
from random import randint, random

# Generate configuration
configs = Configuration.generate_configuration(10)
MAX_POPULATION = 10
MAX_GENERATION = 10
RESPONSE_TIME_GOAL = 600
image_created = False

def generate_population(size: int):
    population = []
    length = len(configs)
    for _ in range(size):
        population.append(Population(length))
    return population

def fitness(trait, response_time_limit : int = 500):
    global image_created
    if (len(trait) != len(configs)):
        raise ValueError("Non existant configuration error")
    
    cpu_count = 0
    cpu_percent = 0
    mem_limit = 0
    total = 0

    if 1 not in trait:
        return 0

    for i in range(len(trait)):
        if trait[i] == 1:
            cpu_count += configs[i].cpu_count
            cpu_percent += configs[i].cpu_percent
            mem_limit += configs[i].mem_limit
            total += 1
    
    new_config = Configuration(cpu_count // total, cpu_percent // total, mem_limit // total)

    # run container with configuration
    web_configuration = {
        "name": "web-stress-test",
        "version": "latest",
        "path": getcwd() + "\\web\\",
        "port": "6969:80",
        "mem_limit": str(new_config.mem_limit) + "m",
        "mem_swappiness": 60,
        "memswap_limit": "100m",
        "cpu_count" : new_config.cpu_count,
        "cpu_percent" : new_config.cpu_percent
    }

    arguments = {
        "URL": "http://192.168.0.107:6969/",
        "connection": 20,
        "output": "result.txt",
        "request": 4096,
        "timeout": 10,
    }

    if not image_created:
        create_image(web_configuration)
        image_created = True

    # run stress test on container
    create_container(web_configuration)

    average_response_time = stress_test(arguments)
    
    if average_response_time > response_time_limit:
        return 0
    
    stop_container(web_configuration)
    
    return average_response_time

def selection(populations):
    next_generation = []
    weights = []
    
    for population in populations:
        population.average_response_time = fitness(population.trait)
        weights.append(population.average_response_time)
    
    for _ in range(int(len(populations) / 2) - 1):
        parents = choices(
            populations, k=2, weights=weights,
        )
        first_parent, second_parent = sp_crossover(parents[0], parents[1])
        first_parent = mutation(first_parent)
        second_parent = mutation(second_parent)
        next_generation += [first_parent, second_parent]

    return next_generation

def mutation(population, probability: float = 0.2):
    for index in range(len(population.trait)):
        
        chance = random()
        
        if chance < probability:
            population.trait[index] = abs(population.trait[index])
    
    return population

def sp_crossover(first_parent, second_parent):
    if len(first_parent.trait) != len(second_parent.trait):
        raise ValueError("One of the solution has a non existant configurations")
    
    length = len(first_parent.trait)
    if length < 2:
        return first_parent, second_parent

    recombination_index = randint(0, length - 1)
    first_parent.trait = first_parent.trait[0: recombination_index] + second_parent.trait[recombination_index:]
    second_parent.trait = second_parent.trait[0:recombination_index] + first_parent.trait[recombination_index:]
    return first_parent, second_parent
        
def main():
    population = generate_population(MAX_POPULATION)

    idx = 0
    for i in range(MAX_POPULATION):
        population = selection(population)

        if population[0].average_response_time <= RESPONSE_TIME_GOAL:
            idx = i
            break
        
    print("Stopped at generation", i)
    
    cpu_count = 0
    cpu_percent = 0
    mem_limit = 0
    total = 0

    for trait in range(len(population[0].trait)):
        if population[idx].trait[trait] == 1:
            cpu_count += configs[trait].cpu_count
            cpu_percent += configs[trait].cpu_percent
            mem_limit += configs[trait].mem_limit
            total += 1
    
    print("The best configuration are:")
    print("CPU COUNT :", cpu_count // total)
    print("CPU PERCENT :", cpu_percent // total, "%")
    print("MEMORY LIMIT :", mem_limit // total, "MB")
    exit()

if __name__ == "__main__":
    main()
