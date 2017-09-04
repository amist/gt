import os
import math
import json
import random
import configparser
import matplotlib.pyplot as plt
# plt.ion()

class TSP(object):
    config = configparser.ConfigParser()
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config.read(config_file)
        self.mutation_prob = self.config.getint('individual', 'mutation_probability')
        
        self.data_file = self.config.get('problem', 'data_file')
        with open(self.data_file, 'r') as f:
            self.cities = json.loads(f.read())
            self.size = len(self.cities)
        
        self.chromosome = [str(x) for x in range(self.size)]
        random.shuffle(self.chromosome)
        
        self.fitness = None
        self.collisions = set()


    def get_fitness(self):
        if self.fitness is None:
            dist = 0
            for i in range(1, self.size):
                x1, y1 = self.cities[self.chromosome[i-1]]
                x2, y2 = self.cities[self.chromosome[i]]
                dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
            self.fitness = dist
        return self.fitness


    def get_child(self, other):
        child = TSP(config_file=self.config_file)
        partition = random.randint(0, len(self.chromosome)-1)
        child.chromosome = self.chromosome[:partition]
        child.chromosome += [x for x in other.chromosome if x not in child.chromosome]
        return child


    def mutate(self, scope_data=None):
        return
        i1 = random.randint(0, self.size-1)
        i2 = random.randint(0, self.size-1)
        temp = self.chromosome[i1]
        self.chromosome[i1] = self.chromosome[i2]
        self.chromosome[i2] = temp


    def print(self):
        plt.clf()
        for city in self.cities:
            x, y = self.cities[city]
            plt.plot(x, y, '*', color='b')
        for i in range(1, self.size):
            x1, y1 = self.cities[self.chromosome[i-1]]
            x2, y2 = self.cities[self.chromosome[i]]
            # plt.arrow(x1, y1, x2-x1, y2-y1, head_width=0.05, head_length=0.1, fc='k', ec='k')
            plt.plot([x1, x2], [y1, y2], color='k')
        plt.show(block=False)
        plt.pause(0.1)
        
        
        
