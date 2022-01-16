from random import choices


class Trait:

    def __init__(self, trait_object):
        self.total_trait = trait_object["total_trait"]
        self.trait = self.generate_traits() if trait_object["trait"] is None else trait_object["trait"]
        self.average_response_time = 0
        self.cpu_count = []
        self.cpu_percent = []
        self.memory_limit = []

    def __dict__(self):
        pass

    def generate_traits(self):
        return choices([0, 1], k=self.total_trait)

    def reset_configuration(self):
        self.average_response_time = 0
        self.cpu_count = []
        self.cpu_percent = []
        self.memory_limit = []

    def get_average_configuration(self):
        total_cpu_count = 0
        total_cpu_percent = 0
        total_memory_limit = 0

        for index in range(len(self.cpu_count)):
            total_cpu_count += self.cpu_count[index]
            total_cpu_percent += self.cpu_percent[index]
            total_memory_limit += self.memory_limit[index]

        try:
            cpu_count = total_cpu_count // len(self.cpu_count)
        except ZeroDivisionError:
            cpu_count = 0
        try:
            cpu_percent = total_cpu_percent // len(self.cpu_percent)
        except ZeroDivisionError:
            cpu_percent = 0
        try:
            memory_limit = str(total_memory_limit // len(self.memory_limit)) + "m"
        except ZeroDivisionError:
            memory_limit = "0m"

        return cpu_count, cpu_percent, memory_limit
