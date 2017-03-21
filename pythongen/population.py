import os
import sys
import configparser
import random

class SimplePopulation(object):
    def __init__(self, individual):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'run.config'))
        
        self.size = config.getint('population', 'size')
        self.expansion_factor = config.getint('population', 'expansion_factor')
        self.population = [individual() for _ in range(self.size)]


    def process_generation(self):
        for _ in range(self.expansion_factor * len(self.population)):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            child = parent1.get_child(parent2)
            self.population.append(child)

        map(lambda x: x.mutate(), self.population)
        self.population.sort(key=lambda x: x.get_fitness(), reverse=True)
        self.population = self.population[:self.size]


    def get_best(self):
        return self.population[0]
