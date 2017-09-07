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
        # type c: chromosome is swaps based of reference route
        self.chromosome_type = self.config.get('individual', 'chromosome_type')
        
        self.chromosome = list(range(self.size))
        random.shuffle(self.chromosome)
        if self.chromosome_type == 'b':
            self.chromosome = list(enumerate(self.chromosome))
            self.chromosome.sort(key=lambda x: x[1])
            
        if self.chromosome_type == 'c':
            self.reference_route = list(range(self.size))
            self.chromosome = [(random.randint(0, self.size-1), random.randint(0, self.size-1)) for _ in range(self.size//2)]
            self.route = None
        
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
        elif self.chromosome_type == 'c':
            if self.route is None:
                self.route = self.reference_route.copy()
                for gene in self.chromosome:
                    # # swap
                    # self.route[gene[0]], self.route[gene[1]] = self.route[gene[1]], self.route[gene[0]]
                    # # put after
                    # self.route.remove(gene[0])
                    # self.route.insert(gene[1], gene[0])
                    # # swap edges
                    a, b = [gene[0], gene[1]] if gene[0] < gene[1] else [gene[1], gene[0]]
                    len1 = len(self.route)
                    bef = self.route.copy()
                    if a == 0:
                        self.route[a:b] = self.route[b-1::-1]
                    else:
                        self.route[a:b] = self.route[b-1:a-1:-1]
                    try:
                        assert len(self.route) == len1
                    except AssertionError:
                        print(bef)
                        print(self.route)
                        print(gene)
                        raise AssertionError
                    
            return str(self.route[i])
        print('returning None for city order', i)
        return None
            # return str(self.chromosome.index(i))
            
            
    def get_fitness(self):
        if self.fitness is None:
            dist = 0
            prev_index = self.city_index_by_order(self.size-1)
            for i in range(self.size):
                cur_index = self.city_index_by_order(i)
                x1, y1 = self.cities[prev_index]
                x2, y2 = self.cities[cur_index]
                dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
                prev_index = cur_index
            
            self.fitness = dist
        return self.fitness
        
        
    # def sort_chromosome(self, ref):
        # keydict = dict(zip(self.chromosome, ref))
        # self.chromosome.sort(key=keydict.get)
        
        
    def normalize_chromosome(self, chromosome):
        chromosome.sort(key=lambda x: x[0])
        offset = chromosome[0][1]
        size = len(chromosome)
        # print()
        # for i in range(len(chromosome)):
            # elem = chromosome[i]
            # print(elem[0], elem[1], '->', (elem[1]-offset+size)%size)
        chromosome = [(city, (order-offset+size)%size) for (city, order) in chromosome]
        chromosome.sort(key=lambda x: x[1])
        return chromosome


    def get_child(self, other):
        child = TSP(config_file=self.config_file)
        if self.chromosome_type == 'a':
            partition = random.randint(0, len(self.chromosome)-1)
            child.chromosome = self.chromosome[:partition]
            child.chromosome += [x for x in other.chromosome if x not in child.chromosome]
        elif self.chromosome_type == 'b':
            partition = random.randint(0, len(self.chromosome)-1)
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
                
            # self.normalize_chromosome(child.chromosome)
            child.chromosome = self.normalize_chromosome(child.chromosome)
        elif self.chromosome_type == 'c':
            if len(self.chromosome) > 0:
                self_partition = random.randint(0, len(self.chromosome)-1)
            else:
                self_partition = 0
            if len(other.chromosome) > 0:
                other_partition = random.randint(0, len(other.chromosome)-1)
            else:
                other_partition = 0
            child.chromosome = []
            child.chromosome += self.chromosome[self_partition:]
            child.chromosome += other.chromosome[:other_partition]
                
        return child


    def mutate(self, scope_data=None):
        if random.randint(0, self.mutation_prob) == 0:
            if self.chromosome_type == 'c':
                if random.randint(0, 10) != 0:
                    self.chromosome.append((random.randint(0, self.size-1),random.randint(0, self.size-1)))
                else:
                    del self.chromosome[random.randint(0, len(self.chromosome)-1)]
            
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
            x1, y1 = self.cities[self.city_index_by_order(0)]
            x2, y2 = self.cities[self.city_index_by_order(self.size-1)]
            plt.plot([x1, x2], [y1, y2], color='y')
            plt.show(block=False)
            plt.pause(0.1)
        else:
            print(self.chromosome)
        
        
