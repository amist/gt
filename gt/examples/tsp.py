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
            
        self.dynamic_mutation = self.config.getboolean('individual', 'dynamic_mutation')
        self.dynamic_mutation_inheritance = self.config.getboolean('individual', 'dynamic_mutation_inheritance')
        self.dynamic_mutation_amplitude = 2
        self.dynamic_mutation_threshold = 0.2
        
        self.smart_crossover = self.config.getboolean('individual', 'smart_crossover')
        
        # type a: route 2 -> 0 -> 1 is chromosome [2,0,1]
        # type b: route 2 -> 0 -> 1 is chromosome [(2,0),(0,1),(1,2)]. each tuple is (city, order) and list is sorted by order.
        # type c: chromosome is swaps based on reference route
        self.chromosome_type = self.config.get('individual', 'chromosome_type')
        
        self.chromosome = list(range(self.size))
        random.shuffle(self.chromosome)
        if self.chromosome_type == 'b':
            self.chromosome = list(enumerate(self.chromosome))
            self.chromosome.sort(key=lambda x: x[1])
            self.cities_matrix = None
            
        if self.chromosome_type == 'c':
            self.reference_solution = list(range(self.size))
            self.chromosome = [(random.randint(0, self.size-1), random.randint(0, self.size-1)) for _ in range(self.size//2)]
            self.route = None
        
        self.output_mode = self.config.get('runner', 'output_mode')
        
        self.fitness = None
        self.collisions = set()
        
        
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
        if self.chromosome_type == 'a':
            return str(self.chromosome[i])
        elif self.chromosome_type == 'b':
            for city, order in self.chromosome:
                if order == i:
                    return str(city)
        elif self.chromosome_type == 'c':
            return str(self.get_solution()[i])
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
            if self.smart_crossover:
                i = other.chromosome.index(self.chromosome[0])
                other_chromosome_1 = other.chromosome[i:] + other.chromosome[:i]
                other_chromosome_2 = [other_chromosome_1[0]] + other_chromosome_1[-1:0:-1]
                assert len(other_chromosome_1) == len(self.chromosome)
                self_set = set()
                other_set_1 = set()
                other_set_2 = set()
                partition_candidates_1 = []
                partition_candidates_2 = []
                for i in range(1, len(self.chromosome)-1):
                    self_set.add(self.chromosome[i])
                    other_set_1.add(other_chromosome_1[i])
                    other_set_2.add(other_chromosome_2[i])
                    if self_set == other_set_1:
                        partition_candidates_1.append(i)
                    if self_set == other_set_2:
                        partition_candidates_2.append(i)
                partition_candidates, other_chromosome = [partition_candidates_1, other_chromosome_1] if len(partition_candidates_1) > len(partition_candidates_2) else [partition_candidates_2, other_chromosome_2]
                partition_candidates = [x for x in partition_candidates if 0.3*len(self.chromosome) < x < 0.6*len(self.chromosome)]
                if len(partition_candidates) == 0:
                    # print('no candidates')
                    partition = random.randint(0, len(self.chromosome)-1)
                else:
                    partition = random.choice(partition_candidates)
                # print(self.chromosome)
                # print(other_chromosome)
                # print('candidates =', partition_candidates)
                # print('partition =', partition)
                child.chromosome = self.chromosome[:partition]
                child.chromosome += [x for x in other_chromosome if x not in child.chromosome]
            else:
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
            child.cities_matrix = self.cities_matrix
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
            
            if self.dynamic_mutation_inheritance:
                child.dynamic_mutation_threshold = self.dynamic_mutation_threshold
                child.dynamic_mutation_amplitude = self.dynamic_mutation_amplitude
                
        return child


    def mutate(self, scope_data=None):
        if self.dynamic_mutation and scope_data is not None:
            good = scope_data['good_mutation']
            bad = scope_data['bad_mutation']
            no = scope_data['no_mutation']
            if good != 0 and bad != 0:
                # mutation_prob = self.mutation_prob // (good / bad)
                mutation_prob = int(self.mutation_prob * (0.25 + (good + bad) / good))
            else:
                mutation_prob = int(self.mutation_prob)
            if self.dynamic_mutation_threshold * good > bad:
                mutation_prob /= self.dynamic_mutation_amplitude
                
                if self.dynamic_mutation_inheritance:
                    self.dynamic_mutation_amplitude += 0.5
                    if self.dynamic_mutation_amplitude > 5:
                        self.dynamic_mutation_amplitude = 5
                    self.dynamic_mutation_threshold -= 0.05
                    if self.dynamic_mutation_threshold < 0.2:
                        self.dynamic_mutation_threshold = 0.2
                        
            else:
                if self.dynamic_mutation_inheritance:
                    self.dynamic_mutation_amplitude -= 0.5
                    if self.dynamic_mutation_amplitude < 2:
                        self.dynamic_mutation_amplitude = 2
                    self.dynamic_mutation_threshold += 0.05
                    if self.dynamic_mutation_threshold > 0.5:
                        self.dynamic_mutation_threshold = 0.5
                        
                
            # print(mutation_prob)
        else:
            mutation_prob = self.mutation_prob
        
        self.fitness = None
        if random.randint(0, mutation_prob) == 0:
            if self.dynamic_mutation or True:
                fitness_before = self.get_fitness()
                self.fitness = None
                
            if self.chromosome_type == 'a':
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
                    
            elif self.chromosome_type == 'b':
                a_index = random.randint(0, self.size-1)
                if self.cities_matrix is None:
                    self.cities_matrix = []
                    for i1 in self.cities:
                        row = []
                        for i2 in self.cities:
                            x1 = self.cities[i1][0]
                            y1 = self.cities[i1][1]
                            x2 = self.cities[i2][0]
                            y2 = self.cities[i2][1]
                            row.append(math.sqrt((x1-x2)**2 + (y1-y2)**2))
                        self.cities_matrix.append(row)
                choice_list = self.cities_matrix[a_index]
                # rank the cities according to their distance from the chosen city
                rank_list = [sorted(choice_list).index(v) for v in choice_list]
                # don't choose the first city - it's the chosen city itself
                b_index = int(random.triangular(1, self.size-1, 1))
                # print(a_index, b_index)
                
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
                self.chromosome = [(city, i) for i, (city, order) in enumerate(self.chromosome)]
        
            elif self.chromosome_type == 'c':
                if random.randint(0, 10) != 0:
                    self.chromosome.append((random.randint(0, self.size-1),random.randint(0, self.size-1)))
                else:
                    if len(self.chromosome) > 0:
                        del self.chromosome[random.randint(0, len(self.chromosome)-1)]
            
            if self.dynamic_mutation or True:
                fitness_after = self.get_fitness()
                # if fitness_after < fitness_before:
                    # print('good one: before = {}, after = {}'.format(fitness_before, fitness_after))
                return fitness_after < fitness_before
        
        return None
        i1 = random.randint(0, self.size-1)
        i2 = random.randint(0, self.size-1)
        temp = self.chromosome[i1]
        self.chromosome[i1] = self.chromosome[i2]
        self.chromosome[i2] = temp


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
                plt.plot([x1, x2], [y1, y2], color='k')
            x1, y1 = self.cities[self.city_index_by_order(0)]
            x2, y2 = self.cities[self.city_index_by_order(self.size-1)]
            plt.plot([x1, x2], [y1, y2], color='y')
            plt.show(block=False)
            plt.pause(interval=0.001)
        elif self.output_mode == 'console':
            print(self.chromosome)
        
        
