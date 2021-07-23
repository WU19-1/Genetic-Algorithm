from main import generate_traits
from random import choices, randint, random
from multiprocessing import cpu_count
from psutil import virtual_memory

MEGABYTE = 1_048_576

MAX_CPU = cpu_count() // 4
MAX_RAM = int(virtual_memory().total) // 4 // MEGABYTE

class Population:
    trait = []
    average_response_time = 0

    def __init__(self, length : int):
        self.trait = generate_traits(length)

    def generate_traits(length : int):
        return choices([0,1],k=length)

class Configuration:
    cpu_count = 0
    cpu_percent = 0
    mem_limit = 0

    def __init__(self, cpu_count, cpu_percent, mem_limit):
        self.cpu_count = cpu_count
        self.cpu_percent = cpu_percent
        self.mem_limit = mem_limit
    
    def generate_configuration(length : int):
        configs = []
        for _ in range(length):
            configs.append(Configuration(
                randint(1, MAX_CPU),
                randint(1,25),
                randint(1,MAX_RAM)
            ))
        
        return configs