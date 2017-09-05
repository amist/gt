import os
import math
import json
import random
import configparser

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
        
        # type a: route 2 -> 0 -> 1 is chromosome [2,0,1]
        # type b: route 2 -> 0 -> 1 is chromosome [(2,0),(0,1),(1,2)]. each tuple is (city, order) and list is sorted by order.
        self.chromosome_type = self.config.get('individual', 'chromosome_type')
        
        self.chromosome = list(range(self.size))
        random.shuffle(self.chromosome)
        if self.chromosome_type == 'b':
            self.chromosome = list(enumerate(self.chromosome))
            self.chromosome.sort(key=lambda x: x[1])
            
        self.graphic_output = self.config.getboolean('runner', 'graphic_output')
        
        self.fitness = None
        self.collisions = set()
        
        
    def city_index_by_order(self, i):
        if self.chromosome_type == 'a':
            return str(self.chromosome[i])
        elif self.chromosome_type == 'b':
            for city, order in self.chromosome:
                if order == i:
                    return str(city)
            return None
            # return str(self.chromosome.index(i))


    def get_fitness(self):
        if self.fitness is None:
            dist = 0
            prev_index = self.city_index_by_order(0)
            for i in range(1, self.size):
                cur_index = self.city_index_by_order(i)
                x1, y1 = self.cities[prev_index]
                x2, y2 = self.cities[cur_index]
                dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
                prev_index = cur_index
            self.fitness = dist
        return self.fitness


    def get_child(self, other):
        child = TSP(config_file=self.config_file)
        partition = random.randint(0, len(self.chromosome)-1)
        if self.chromosome_type == 'a':
            child.chromosome = self.chromosome[:partition]
            child.chromosome += [x for x in other.chromosome if x not in child.chromosome]
        elif self.chromosome_type == 'b':
            child.chromosome = self.chromosome[:partition]
            # other_chromosome = other.chromosome.copy()
            # other_chromosome.sort(key=lambda x: x[1])
            existing_cities = [x[0] for x in child.chromosome]
            existing_orders = [x[1] for x in child.chromosome]
            order_index = 0
            # while len(child.chromosome < self.size):
            for gene in other.chromosome:
                if gene[0] in existing_cities:
                    continue
                while order_index in existing_orders:
                    order_index += 1
                child.chromosome.append((gene[0], order_index))
                existing_cities.append(gene[0])
                existing_orders.append(order_index)
            child.chromosome.sort(key=lambda x: x[1])
                
        return child


    def mutate(self, scope_data=None):
        return
        i1 = random.randint(0, self.size-1)
        i2 = random.randint(0, self.size-1)
        temp = self.chromosome[i1]
        self.chromosome[i1] = self.chromosome[i2]
        self.chromosome[i2] = temp


    def print(self):
        if self.graphic_output:
            import matplotlib.pyplot as plt
            plt.clf()
            for city in self.cities:
                x, y = self.cities[city]
                plt.plot(x, y, '*', color='b')
            for i in range(1, self.size):
                x1, y1 = self.cities[self.city_index_by_order(i-1)]
                x2, y2 = self.cities[self.city_index_by_order(i)]
                # plt.arrow(x1, y1, x2-x1, y2-y1, head_width=0.05, head_length=0.1, fc='k', ec='k')
                plt.plot([x1, x2], [y1, y2], color='k')
            plt.show(block=False)
            plt.pause(0.1)
        else:
            print(self.chromosome)
        
        
