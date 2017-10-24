import os
import gc
import math
import json
import random
import configparser

class TSPMultiple(object):
    config = configparser.ConfigParser()
    
    cities = None
    order = None
    
    def __init__(self, config, start_point_ratio=0, const_data=None):
        self.config = config
        self.const_data = const_data
        
        if const_data is None:
            if TSPMultiple.cities is None:
                self.data_file = self.config.get('problem', 'data_file')
                with open(self.data_file, 'r') as f:
                    TSPMultiple.cities = json.loads(f.read())
                
            if TSPMultiple.order is None:
                self.order_file = self.config.get('problem', 'order_file')
                with open(self.order_file, 'r') as f:
                    TSPMultiple.order = json.loads(f.read())
                    # self.temp_order = json.loads(f.read())
                    # self.order = {}
                    # for city in self.cities.keys():
                        # self.order[city] = self.temp_order[city]
                    # del self.temp_order
                    # gc.collect()
        else:
            TSPMultiple.cities = const_data['cities']
            TSPMultiple.order = const_data['order']
            
        try:
            self.start_point = self.config.getint('individual', 'start_point')
            self.start_point_ratio = self.start_point // (len(TSPMultiple.cities)-1)
            self.start_point = str(self.start_point)
        except configparser.NoOptionError:
            self.start_point_ratio = start_point_ratio
            self.start_point = str(int((len(TSPMultiple.cities)-1) * start_point_ratio))
            
        self.mutation_prob = self.config.getint('individual', 'mutation_probability')
        
        self.size = self.config.getint('individual', 'size')
        self.chromosome = [x[0] for x in TSPMultiple.order[self.start_point][:self.size]]
        random.shuffle(self.chromosome)
        # print(self.chromosome)

        self.output_mode = self.config.get('runner', 'output_mode')
        
        self.fitness = None
        
        
    def expand_chromosome(self):
        if len(self.chromosome) == len(TSPMultiple.cities):
            return True
        # print(self.chromosome)
        # n = self.order[self.start_point][self.size][0]      # that's the old calculation, but with merges it doesn't necessarily need to be the size-th element
        to_add = -1
        for i in range(len(TSPMultiple.cities)):
            n = TSPMultiple.order[self.start_point][i][0]
            if n not in self.chromosome:
                to_add = i
                break
        # print(n)
        try:
            # after = self.order[self.start_point][self.size][1]  # the old code
            after = TSPMultiple.order[self.start_point][to_add][1]
            index = self.chromosome.index(after)
        except ValueError:
            print(self.chromosome)
            print(len(self.chromosome))
            print(self.size)
            print(self.start_point)
            print(TSPMultiple.order[self.start_point])
            print(n)
            raise ValueError
            
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
                x1, y1 = TSPMultiple.cities[str(self.chromosome[i-1])]
                x2, y2 = TSPMultiple.cities[str(self.chromosome[i])]
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
        child = TSPMultiple(config=self.config, start_point_ratio=self.start_point_ratio, const_data=self.const_data)
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
            print(self.chromosome, other.chromosome, child.chromosome)
            # print(len(child.chromosome), len(self.chromosome), len(other.chromosome))
            # child.chromosome = child.chromosome[:child.size]
            # return None
            print('different size crossover')
        
        # print('creating', child.chromosome, 'id =', id(child.chromosome))
        child.size = self.size
        child.start_point = self.start_point
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
        self_print = True       # false when print is handles by population (since this is only part of the solution)
        if self.output_mode == 'graphic':
            import matplotlib.pyplot as plt
            if self_print:
                plt.clf()
                plt.suptitle('fitness = {}'.format(self.get_fitness()))
            for city in TSPMultiple.cities:
                x, y = TSPMultiple.cities[city]
                plt.plot(x, y, '.', color='b')
            for i in range(1, self.size):
                x1, y1 = TSPMultiple.cities[self.city_index_by_order(i-1)]
                x2, y2 = TSPMultiple.cities[self.city_index_by_order(i)]
                plt.plot([x1, x2], [y1, y2], color='k')
            x1, y1 = TSPMultiple.cities[self.city_index_by_order(0)]
            x2, y2 = TSPMultiple.cities[self.city_index_by_order(self.size-1)]
            plt.plot([x1, x2], [y1, y2], color='k')
            if self_print:
                plt.show(block=False)
                plt.pause(interval=0.001)
        elif self.output_mode == 'console':
            print(self.chromosome)
        
        
