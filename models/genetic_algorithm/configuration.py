from random import randint
from multiprocessing import cpu_count
from psutil import virtual_memory

MEGABYTE = 1_048_576
# MAX_RAM = int(virtual_memory().total) // MEGABYTE

class Configuration:
    MAX_CPU = 1
    MAX_CPU_PERCENTAGE = 100
    MAX_RAM = int(virtual_memory().total) // MEGABYTE
    MIN_RAM = 512

    def __init__(self, configuration_object=None):
        self.MAX_CPU = configuration_object["max_cpu_count"]
        self.MAX_CPU_PERCENTAGE = configuration_object["max_cpu_percentage"]
        self.MIN_RAM = configuration_object["min_ram"]
        self.MAX_RAM = configuration_object["max_ram"]
        self.cpu_count = randint(1, self.MAX_CPU)
        self.cpu_percent = randint(1, self.MAX_CPU_PERCENTAGE)
        self.memory_limit = randint(self.MIN_RAM, self.MAX_RAM)