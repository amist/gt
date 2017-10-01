import os
import math
import json
import random
import configparser

class TSPEvolve(object):
    config = configparser.ConfigParser()
    
    def __init__(self, config, const_data=None):
        # self.config_file = config_file
        # self.config.read(config_file)
        self.config = config
        self.const_data = const_data
        self.start_point = '0'
        
        if const_data is None:
            self.data_file = self.config.get('problem', 'data_file')
            with open(self.data_file, 'r') as f:
                self.cities = json.loads(f.read())
                # self.size = len(self.cities)
                
            self.order_file = self.config.get('problem', 'order_file')
            with open(self.order_file, 'r') as f:
                self.order = json.loads(f.read())[self.start_point]
        else:
            self.cities = const_data['cities']
            # self.size = len(self.cities)
            self.order = const_data['order']
            self.start_point = const_data['start_point']
            
        self.mutation_prob = self.config.getint('individual', 'mutation_probability')
        
        self.size = 4
        self.chromosome = [x[0] for x in self.order[:self.size]]
        random.shuffle(self.chromosome)
        # print(self.chromosome)

        self.output_mode = self.config.get('runner', 'output_mode')
        
        self.fitness = None
        
        
    def expand_chromosome(self):
        if len(self.chromosome) == len(self.cities):
            return True
        # print(self.chromosome)
        n = self.order[self.size][0]
        # print(n)
        after = self.order[self.size][1]
        index = self.chromosome.index(after)
        self.chromosome = self.chromosome[:index] + [n] + self.chromosome[index:]
        self.size = len(self.chromosome)
        # print(self.chromosome)
        return False
        
        
    def get_solution(self):
        if self.route is None:
            self.route = self.reference_solution.copy()
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
                if b == 0:
                    continue
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
        
        return self.route
        
        
    def city_index_by_order(self, i):
        return str(self.chromosome[i])
            
            
    def get_fitness(self, generation=None):
        if self.fitness is None:
            dist = 0
            for i in range(self.size):
                x1, y1 = self.cities[str(self.chromosome[i-1])]
                x2, y2 = self.cities[str(self.chromosome[i])]
                dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
            self.fitness = dist
            
        return self.fitness
        
        
    def get_child(self, other):
        if len(self.chromosome) > self.size:
            # print('fixing self.chromosome')
            self.chromosome = self.chromosome[:self.size]
        if len(other.chromosome) > other.size:
            # print('fixing other.chromosome')
            other.chromosome = other.chromosome[:other.size]
        # print('begin get child')
        # print(self.chromosome, id(self.chromosome))
        # print(other.chromosome, id(other.chromosome))
        child = TSPEvolve(config=self.config, const_data=self.const_data)
        # if self is other:
            # print('self is other')
            # return child
        
        partition = random.randint(0, len(self.chromosome)-1)
        child.chromosome = self.chromosome[:partition]
        # print(partition)
        assert id(child.chromosome) != id(self.chromosome)
        assert id(child.chromosome) != id(other.chromosome)
        child.chromosome += [x for x in other.chromosome if x not in child.chromosome]
        
        if id(child.chromosome) == id(other.chromosome):
            print(partition)
        if id(child.chromosome) == id(self.chromosome):
            print(partition)
        # print('middle get child')
        # print(self.chromosome)
        # print(other.chromosome)
        # print(child.chromosome)
        try:
            assert len(child.chromosome) == len(self.chromosome) == len(other.chromosome)
        except AssertionError:
            # print(len(child.chromosome), len(self.chromosome), len(other.chromosome))
            # child.chromosome = child.chromosome[:child.size]
            return None
        
        # print('creating', child.chromosome, 'id =', id(child.chromosome))
        child.size = self.size
        return child


    def mutate(self, scope_data=None):
        mutation_prob = self.mutation_prob
        
        self.fitness = None
        if random.randint(0, mutation_prob) == 0:
            a_index = random.randint(0, self.size-1)
            b_index = random.randint(0, self.size-1)
            if a_index > b_index:
                a_index, b_index = b_index, a_index
            if random.randint(0,1) == 0:
                # swap edges
                if a_index == 0:
                    self.chromosome[a_index:b_index] = self.chromosome[b_index-1::-1]
                else:
                    self.chromosome[a_index:b_index] = self.chromosome[b_index-1:a_index-1:-1]
            else:
                # insert node after node
                node = self.chromosome.pop(a_index)
                self.chromosome.insert(b_index, node)
                    
        return None


    def print(self):
        if self.output_mode == 'graphic':
            import matplotlib.pyplot as plt
            plt.clf()
            plt.suptitle('fitness = {}'.format(self.get_fitness()))
            for city in self.cities:
                x, y = self.cities[city]
                plt.plot(x, y, '*', color='b')
            for i in range(1, self.size):
                x1, y1 = self.cities[self.city_index_by_order(i-1)]
                x2, y2 = self.cities[self.city_index_by_order(i)]
                plt.plot([x1, x2], [y1, y2], color='k')
            x1, y1 = self.cities[self.city_index_by_order(0)]
            x2, y2 = self.cities[self.city_index_by_order(self.size-1)]
            plt.plot([x1, x2], [y1, y2], color='y')
            plt.show(block=False)
            plt.pause(interval=0.001)
        elif self.output_mode == 'console':
            print(self.chromosome)
        
        
