import typing
from random import choices
from random import randint
from random import random
from functools import partial
from collections import namedtuple

Trait = typing.List[int]
Population = typing.List[Trait]
Item = namedtuple('Item', tuple(['name','weight','value']))
FitnessFunction = typing.Callable[[Trait],int]
PopulateFunction = typing.Callable[[], Population]
SelectionFunction = typing.Callable[[Population, FitnessFunction],Population]
CrossoverFunction = typing.Callable[[Trait, Trait], typing.Tuple[Trait, Trait]]
MutationFunction = typing.Callable[[Trait, float], Trait]

items = [
    Item("Laptop A", 10, 60),
    Item("Laptop B", 20, 100),
    Item("Laptop C", 30, 120),
]

def generate_traits(length: int) -> Trait:
    return choices([0,1],k=length)

def generate_population(size: int, trait_length: int) -> Population:
    return [generate_traits(trait_length) for _ in range(0,size)]

def fitness(trait: Trait, items: [Item], limit: int) -> int:
    if len(trait) != len(items):
        raise ValueError("You can't stole a non existant item! :)")
    
    weight = 0
    value = 0

    for i, thing in enumerate(items):
        if trait[i] == 1:
            weight += thing.weight
            value += thing.value
        
            if weight > limit:
                return 0

    return value

def selection(population: Population, fitness_function: FitnessFunction) -> Population:
    return choices(
        population=population,
        weights=[fitness_function(trait) for trait in population],
        k=2
    )

def sp_crossover(first_parent: Trait, second_parent: Trait) -> typing.Tuple[Trait,Trait]:
    if len(first_parent) != len(second_parent):
        raise ValueError("One of the solution has a non existant items")
    
    length = len(first_parent)
    if length < 2:
        return first_parent, second_parent

    recombination_index = randint(0, length - 1)
    return first_parent[0: recombination_index] + second_parent[recombination_index:], second_parent[0:recombination_index] + first_parent[recombination_index:]

def mutation(trait: Trait, probability: float = 0.5) -> Trait:
    for index in range(len(trait)):
        
        chance = random()
        
        if chance < probability:
            trait[index] = abs(trait[index])
    
    return trait

def run(
    populate_function: PopulateFunction,
    fitness_function: FitnessFunction,
    fitness_limit: int,
    selection_function: SelectionFunction = selection,
    crossover_function: CrossoverFunction = sp_crossover,
    mutation_function: MutationFunction = mutation,
    generation_limit: int = 100
) -> typing.Tuple[Population, int]:
    population = populate_function()
    for i in range(generation_limit):
        
        population = sorted(population,key=lambda trait: fitness_function(trait), reverse=True)

        if fitness_function(population[0]) >= fitness_limit:
            break

        next_generation = population[0:3]

        for j in range(int(len(population) / 2 - 1)):
            parents = selection_function(population, fitness_function)
            first_children, second_children = crossover_function(parents[0], parents[1])
            first_children = mutation_function(first_children)
            second_children = mutation_function(second_children)
            next_generation += [first_children, second_children]

        population = next_generation

    population = sorted(population,key=lambda trait: fitness_function(trait), reverse=True)

    return population, i

def trait_to_items(trait: Trait, items: [Item])-> [Item]:
    result = []
    for i, item in enumerate(items):
        if trait[i] == 1:
            result += [item.name]

    return result

def main():
    population, generations = run(
        populate_function=partial(
            generate_population, size=10, trait_length=len(items)
        ),
        fitness_function=partial(
            fitness, items=items, limit=50
        ),
        fitness_limit=220,
        generation_limit=100
    )

    print("Number of generations:", generations)
    print("Best solution:", trait_to_items(population[0], items))


if __name__ == "__main__":
    main()