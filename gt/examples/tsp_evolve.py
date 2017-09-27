import os
import math
import json
import random
import configparser

class TSPEvolve(object):
    config = configparser.ConfigParser()
    
    def __init__(self, config):
        # self.config_file = config_file
        # self.config.read(config_file)
        self.config = config
        
        self.data_file = self.config.get('problem', 'data_file')
        with open(self.data_file, 'r') as f:
            self.cities = json.loads(f.read())
            self.size = len(self.cities)
            
        self.order_file = self.config.get('problem', 'order_file')
        with open(self.order_file, 'r') as f:
            self.order = json.loads(f.read())
            
        self.mutation_prob = self.config.getint('individual', 'mutation_probability')
            
        self.up_to = self.size      # the point in route up to which the fitness is calculated
        self.generations_evolution_step = self.config.getint('individual', 'generations_evolution_step')
        self.evolution_start = self.config.getint('individual', 'evolution_start')
            
        self.chromosome = list(range(self.size))
        random.shuffle(self.chromosome)

        self.output_mode = self.config.get('runner', 'output_mode')
        
        self.fitness = None
        
        
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
            self.fitness = -1
        return self.fitness
        
        
    def get_child(self, other):
        child = TSPEvolve(config=self.config)
        
        self_real = [x for x in self.chromosome if x in self.order[:self.up_to]]
        # print(self.up_to)
        # print(self_real)
        other_real = [x for x in other.chromosome if x in self.order[:self.up_to]]
        try:
            assert len(self_real) == len(other_real)
        except AssertionError:
            print(self.chromosome)
            print(other.chromosome)
            print(self_real)
            print(other_real)
            raise AssertionError
        assert set(self_real) == set(other_real)
        
        partition = random.randint(0, len(self_real)-1)
        # child.chromosome = self_real[:partition] + other_real[partition:]
        child.chromosome = self_real[:partition] + [x for x in other_real if x not in self_real[:partition]]
        assert len(child.chromosome) == len(self_real)
        self_junk = [x for x in self.chromosome if x not in child.chromosome]
        random.shuffle(self_junk)
        child.chromosome += self_junk
        try:
            assert len(child.chromosome) == len(self.chromosome)
            assert len(child.chromosome) == self.size
        except AssertionError:
            print(self_real)
            print(other_real)
            print(self_junk)
            print(partition)
            print(child.chromosome)
            raise AssertionError
            
        return child


    def mutate(self, scope_data=None):
        mutation_prob = self.mutation_prob
        
        self.fitness = None
        if random.randint(0, mutation_prob) == 0:
            a_index = self.chromosome.index(random.choice(self.order[:self.up_to]))
            b_index = self.chromosome.index(random.choice(self.order[:self.up_to]))
            
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
                # plt.arrow(x1, y1, x2-x1, y2-y1, head_width=0.05, head_length=0.1, fc='k', ec='k')
                if int(self.city_index_by_order(i)) in self.order[:self.up_to]:
                    plt.plot([x1, x2], [y1, y2], color='k')
                else:
                    ...
                    # plt.plot([x1, x2], [y1, y2], color='y')
            x1, y1 = self.cities[self.city_index_by_order(0)]
            x2, y2 = self.cities[self.city_index_by_order(self.size-1)]
            plt.plot([x1, x2], [y1, y2], color='y')
            plt.show(block=False)
            plt.pause(interval=0.001)
        elif self.output_mode == 'console':
            print(self.chromosome)
        
        
