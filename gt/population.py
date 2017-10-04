import os
import sys
import json
import copy
import configparser
import random
import logging
import datetime
from gt.examples.tsp import TSP


class BasePopulation(object):
    def expand_population(self):
        for _ in range(self.expansion_factor * len(self.population)):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            # parent1 = self.population[int(random.triangular(0, self.size-1, 0))]
            # parent2 = self.population[int(random.triangular(0, self.size-1, 0))]
            child = parent1.get_child(parent2)
            self.population.append(child)
            
            
    def show_diversity_info(self):
        best_chromosome = self.population[0].chromosome
        worst_chromosome = self.population[-1].chromosome
        


class SimplePopulation(BasePopulation):
    def __init__(self, individual, config_file=None, config_string=None):
        config = configparser.ConfigParser()
        if config_file is not None:
            config.read(config_file)
        else:
            config.read_string(config_string)
        
        self.individual_class = individual
        self.config_file = config_file
        
        self.scope_data = None
        
        self.size = config.getint('population', 'size')
        self.expansion_factor = config.getint('population', 'expansion_factor')
        self.expansion_type = config.get('population', 'expansion_type')
        
        self.evolution_type = config.get('population', 'evolution_type')
        self.ch_expansion_finished = False
        
        self.config_mode = config.get('runner', 'config_mode')
        if self.config_mode == 'file':
            self.population = [individual(config_file=config_file) for _ in range(self.size)]
        elif self.config_mode == 'object':
            self.population = [individual(config=config) for _ in range(self.size)]
        self.generation = 0
        
        try:
            self.initial_population = config.get('population', 'initial_population')
        except configparser.NoOptionError:
            self.initial_population = ''
        if self.initial_population != '':
            with open(self.initial_population) as f:
                chromosomes = json.load(f)
            # chromosomes = json.load(self.initial_population)
            self.size = len(chromosomes)
            self.population = self.population[:self.size]
            for i, chromosome in enumerate(chromosomes):
                self.population[i].chromosome = chromosome
                self.population[i].size = len(chromosome)
        
        for i, individual in enumerate(self.population):
            try:
                assert len(individual.chromosome) == individual.size
            except AssertionError:
                print('In init!!! removing corrupted individual', i, individual.chromosome)
                self.population.remove(individual)  # ugly
        
    def reset_population(self):
        return
        if self.population[0].chromosome_type == 'c':
            ref_solution = self.population[0].get_solution()
            self.population = [self.individual_class(config_file=self.config_file) for _ in range(self.size)]
            for individual in self.population:
                individual.reference_solution = ref_solution
            self.population[0].chromosome = []
            
            
    def expand_population(self):
        for xx in range(self.expansion_factor * len(self.population)):
            if self.expansion_type == 'unified':
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)
            elif self.expansion_type == 'weighted':
                fitnesses = [x.get_fitness() for x in self.population]
                max_fitness = max(fitnesses)
                fitnesses = [1 + max_fitness - x for x in fitnesses]
                try:
                    parent1, parent2 = random.choices(self.population, weights=fitnesses, k=2)
                except IndexError:
                    print(len(self.population))
                    raise IndexError
            elif self.expansion_type == 'factor_weighted':
                fitnesses = [x.get_fitness() * 10 for x in self.population]
                max_fitness = max(fitnesses)
                fitnesses = [1 + max_fitness - x for x in fitnesses]
                parent1, parent2 = random.choices(self.population, weights=fitnesses, k=2)
            elif self.expansion_type == 'different':
                k = 3
                fitnesses = [x.get_fitness() for x in self.population]
                max_fitness = max(fitnesses)
                fitnesses = [1 + max_fitness - x for x in fitnesses]
                candidates = random.choices(self.population, weights=fitnesses, k=k)
                parent1 = candidates[0]
                pairs = [(parent1.chromosome[i], parent1.chromosome[i+1]) for i in range(len(parent1.chromosome)-1)]
                pairs.append((parent1.chromosome[0], parent1.chromosome[-1]))
                # print(pairs)
                min_count = len(parent1.chromosome)+1
                parent2 = None
                for i in range(1,k):
                    candidate = candidates[i]
                    c_pairs = [(candidate.chromosome[i], candidate.chromosome[i+1]) for i in range(len(candidate.chromosome)-1)]
                    c_pairs.append((candidate.chromosome[0], candidate.chromosome[-1]))
                    count = 0
                    for (x,y) in c_pairs:
                        if (x,y) in pairs or (y,x) in pairs:
                            count += 1
                        if count < min_count:
                            min_count = count
                            parent2 = candidate
            # parent1 = self.population[int(random.triangular(0, self.size-1, 0))]
            # parent2 = self.population[int(random.triangular(0, self.size-1, 0))]
            # print('creating', xx)
            child = parent1.get_child(parent2)
            if child is not None:
                try:
                    # assert len(child.chromosome) == len(parent1.chromosome) == len(parent2.chromosome)
                    assert id(child.chromosome) != id(parent1.chromosome)
                    assert id(child.chromosome) != id(parent2.chromosome)
                except AssertionError:
                    print(id(child.chromosome), id(parent1.chromosome), id(parent2.chromosome))
                    raise AssertionError
                
                self.population.append(child)
                
            # for individual in self.population:
                # print(len(individual.chromosome))
            
            # print('printing all population')
            # for i, individual in enumerate(self.population):
                # print(i, individual.chromosome, id(individual.chromosome))
            
            # for i, individual in enumerate(self.population):
                # try:
                    # assert len(individual.chromosome) == individual.size
                # except AssertionError:
                    # print('during expand, identified corrupted', i, individual.chromosome)
                

    def process_generation(self):
        self.expand_population()

        # min_val = min([min([x for x in i.chromosome]) for i in self.population])
        # max_val = max([max([x for x in i.chromosome]) for i in self.population])
        # scope_data = None
        # min_val = 1
        # max_val = 9
        # scope_data = {'min_val': min_val, 'max_val': max_val}
        # print(scope_data)
        
        # TODO: mutate only the newcomers
        mutation_res = list(map(lambda x: x.mutate(scope_data=self.scope_data), self.population))
        no_mutation = sum([1 for x in mutation_res if x is None])
        bad_mutation = sum([1 for x in mutation_res if x == False])
        good_mutation = sum([1 for x in mutation_res if x == True])
        self.scope_data = {'no_mutation': no_mutation, 'bad_mutation': bad_mutation, 'good_mutation': good_mutation}
        # print(no_mutation, bad_mutation, good_mutation)
        # [x.mutate() for x in self.population]
        
        # ids = set()
        # for individual in self.population:
            # cur = id(individual.chromosome)
            # assert cur not in ids
            # ids.add(cur)
        for i, individual in enumerate(self.population):
            try:
                assert len(individual.chromosome) == individual.size
            except AssertionError:
                before = individual.chromosome[:]
                individual.chromosome = individual.chromosome[:individual.size]
                # print('fixinfixing currupted:', before, '->', individual.chromosome)
                # print('removing corrupted individual', i, individual.chromosome)
                self.population.remove(individual)  # ugly
                # raise AssertionError
        self.population.sort(key=lambda x: x.get_fitness(self.generation), reverse=False)
        self.population = self.population[:self.size]
        
        self.generation += 1
        # if self.generation % 50 == 0:
            # self.reset_population()     # does nothing
        # else:
        if self.evolution_type == 'simple':
            if self.population[0].chromosome == self.population[-1].chromosome:
                return 'convergence'
                
        if self.evolution_type == 'progressive':
            # if self.generation % 10 == 0:
            if self.population[0].chromosome == self.population[-1].chromosome:
                for individual in self.population:
                    self.ch_expansion_finished = individual.expand_chromosome()
            
        # sort_chromosome = getattr(self.population[0], "sort_chromosome", None)
        # if callable(sort_chromosome):
            # order = []
            # for individual in population:
                # individual.sort_chromosome(order)
                
    def print_best(self):
        self.population[0].print()

    def get_best(self):
        return self.population[0]
        
    def get_best_chromosome(self):
        return self.population[0].chromosome


class TypesPopulation(BasePopulation):
    def __init__(self, individual, config_file='test.config'):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), config_file))

        self.size = config.getint('population', 'size')
        self.expansion_factor = config.getint('population', 'expansion_factor')
        self.population = [individual() for _ in range(self.size)]

    def process_generation(self):
        try:
            # divide the population into types
            types_populations = {}
            for individual in self.population:
                if individual.type not in types_populations:
                    types_populations[individual.type] = []
                types_populations[individual.type].append(individual)

            # assuming there are two types
            types = list(types_populations.keys())
            for _ in range(self.expansion_factor * len(self.population)):
                parent1 = random.choice(types_populations[types[0]])
                parent2 = random.choice(types_populations[types[1]])
                child = parent1.get_child(parent2)
                child.mutate()
                types_populations[child.type].append(child)

        except AttributeError:
            # no types - handle as SimplePopulation
            print('AttributeError')
            self.expand_population()
            list(map(lambda x: x.mutate(), self.population))
            self.population.sort(key=lambda x: x.get_fitness(), reverse=False)
            self.population = self.population[:self.size]
            return

        self.population = []
        for population_type in types_populations:
            population = types_populations[population_type]
            # list(map(lambda x: x.mutate(), population))
            population.sort(key=lambda x: x.get_type_fitness(), reverse=False)
            population = population[:self.size]
            self.population += population
        self.population.sort(key=lambda x: x.get_fitness(), reverse=False)

    def get_best(self):
        return self.population[0]

        
class TspPopulation(BasePopulation):
    def __init__(self, individual, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        self.individual_class = individual
        
        self.size = config.getint('population', 'size')
        self.expansion_factor = config.getint('population', 'expansion_factor')
        self.expansion_type = config.get('population', 'expansion_type')
        
        self.evolution_type = 'progressive'
        self.ch_expansion_finished = False
        
        self.config_mode = config.get('runner', 'config_mode')
        self.output_mode = config.get('runner', 'output_mode')
        
        self.population = []
        start_point_ratios = [0, 0.25, 0.5, 0.75]
        self.types_number = len(start_point_ratios)
        for start_point_ratio in start_point_ratios:
            self.population += [individual(config=config, start_point_ratio=start_point_ratio) for _ in range(self.size)]
        self.generation = 0
        self.last_expansion = 0
        # for individual in self.population:
            # print(individual)
        
        
    def expand_population(self):
        self.current_types = set()
        for individual in self.population:
            self.current_types.add(individual.start_point)
            
        temp_populations = [[individual for individual in self.population if individual.start_point == start_point] for start_point in self.current_types]
        
        for temp_population in temp_populations:        
            fitnesses = [x.get_fitness() for x in temp_population]
            max_fitness = max(fitnesses)
            fitnesses = [1 + max_fitness - x for x in fitnesses]
            for xx in range(self.expansion_factor * len(temp_population)):
                # TODO: choose according to type
                try:
                    parent1, parent2 = random.choices(temp_population, weights=fitnesses, k=2)
                except IndexError:
                    print(len(temp_population))
                    raise IndexError
                    
                child = parent1.get_child(parent2)
                    
                self.population.append(child)
            
            
    def process_generation(self):
        # for individual in self.population:
            # print(individual.chromosome)
            # print(individual.get_fitness())
        self.expand_population()
        
        map(lambda x: x.mutate(), self.population[self.size:])
        
        self.current_types = set()
        for individual in self.population:
            self.current_types.add(individual.start_point)
            
        temp_populations = [[individual for individual in self.population if individual.start_point == start_point] for start_point in self.current_types]
        
        if len(temp_populations) == 1:
            self.ch_expansion_finished = True
        
        self.generation += 1
        if self.population[0].chromosome == self.population[-1].chromosome:
            if len(self.population[0].chromosome) == len(self.population[0].cities):
                return 'convergence'
            
        current_chromosomes = [set(temp_population[0].chromosome) for temp_population in temp_populations]
        max_size = max([len(c) for c in current_chromosomes])
        if (self.generation - self.last_expansion) % (1 + max_size) == 0:
            self.last_expansion = self.generation
            for individual in self.population:
                individual.expand_chromosome()
                individual.fitness = None
                # temp_populations = [[individual for individual in self.population if individual.start_point == start_point] for start_point in current_types]

        # merge types
        current_chromosomes = [set(temp_population[0].chromosome) for temp_population in temp_populations]
        # print(current_chromosomes)
        
        merge_values = self.what_to_merge(current_chromosomes)
        if merge_values is not None:
            a, b = merge_values
            # print('going to merge', a, b)
            
            new_population = []
            assert len(temp_populations[a]) == len(temp_populations[b])
            for i in range(len(temp_populations[a])):
                parent1 = temp_populations[a][i]
                parent2 = temp_populations[b][i]
                new_chromosome = parent1.chromosome
                new_chromosome += [x for x in parent2.chromosome if x not in new_chromosome]
                child = copy.copy(parent1)
                child.chromosome = new_chromosome
                child.size = len(new_chromosome)
                # child = temp_populations[a][i].get_child(temp_populations[b][i])
                
                new_population.append(child)
                
            temp_populations[a] = temp_populations[b] = []
            temp_populations.append(new_population)
            
            
        self.population = []
        for temp_population in temp_populations:
            temp_population.sort(key=lambda x: x.get_fitness(self.generation), reverse=False)
            temp_population = temp_population[:self.size]
            # print(temp_population)
            self.population += temp_population
            
        # print(self.population)
        
        
        # for individual in self.population:
            # print(individual)
        self.population.sort(key=lambda x: x.get_fitness(self.generation), reverse=False)
        # self.population = self.population[:self.size * self.types_number]
    
    
    def what_to_merge(self, current_chromosomes):
        for i in range(len(current_chromosomes)-1):
            for j in range(i+1, len(current_chromosomes)):
                # print('compare', i, j)
                len_intersection = len(current_chromosomes[i] & current_chromosomes[j])
                min_len = min(len(current_chromosomes[i]), len(current_chromosomes[j]))
                # print('lengths:', len_intersection, min_len)
                if len_intersection > 0.25 * min_len:       # TODO: change it to 2 (and change the merge method accordingly)
                    return i, j     # maximum one merge per generation
        return None
    
    
    def get_best(self):
        return self.population[0]
        
    def get_best_chromosome(self):
        temp_populations = [[individual for individual in self.population if individual.start_point == start_point] for start_point in self.current_types]
        ch = []
        for temp_population in temp_populations:
            # temp_population[0].print()
            ch.append(temp_population[0].chromosome)
        return ch
        
    def print_best(self):
        self.current_types = set()
        for individual in self.population:
            self.current_types.add(individual.start_point)
            
        temp_populations = [[individual for individual in self.population if individual.start_point == start_point] for start_point in self.current_types]
        
        if self.output_mode == 'console':
            print(self.get_best_chromosome())
        elif self.output_mode == 'graphic':
            import matplotlib.pyplot as plt
            plt.clf()
            
            total_fitness = 0
            for temp_population in temp_populations:
                temp_population[0].print()
                # print(temp_population[0].get_fitness())
                total_fitness += temp_population[0].get_fitness()
            
            fitness = sum([temp_population[0].get_fitness() for temp_population in temp_populations])
            # print(fitness)
            plt.suptitle('fitness = {}'.format(fitness))
            plt.show(block=False)
            plt.pause(interval=0.001)
            
            
class MergerPopulation(BasePopulation):
    def __init__(self, individual_util):
        self.size = 100
        self.expansion_factor = 5
        self.partials_population = []
        self.partials_size = 0
        self.iu = individual_util
        self.generations_number = 200
        
        self.population = None
        
        self.logger = logging.getLogger('result')
        self.logger.setLevel(logging.DEBUG)
        fileh = logging.FileHandler('logs/logfile_{}.log'.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', '.')))
        formatter = logging.Formatter('%(message)s')
        fileh.setFormatter(formatter)
        self.logger.addHandler(fileh) 
        
        
    def initialize_process(self, config_string):
        self.config_string = config_string
        # self.logger.info('merger population run')
        # self.logger.info(self.partials_population)
        self.partials_size = len(set([item for sublist in self.partials_population for item in sublist]))
        self.logger.info(config_string)
        self.logger.info('---')
        
        
    def run_merged(self, p1, p2):
        population = SimplePopulation(TSP, config_string=self.config_string)
        population.population = []
        for _ in range(self.size):
            new = self.iu.merge(p1, p2)
            try:
                assert len(new) == len(set(new))
            except AssertionError:
                print(new)
            tsp = TSP(config_string=self.config_string)
            tsp.chromosome = new
            tsp.size = len(new)
            population.population.append(tsp)
        population.size = len(population.population)
        
        for ind in population.population:
            try:
                assert len(ind.chromosome) == len(set(ind.chromosome))
            except AssertionError:
                print(ind.chromosome)
        
        # population.print_best()
        for i in range(self.generations_number):
            population.process_generation()
            ch = population.population[0].chromosome
            
            print('Generation: {:2}: Chromosome Size: {}, Partial Fitness: {:3}'.format(i, len(ch), population.get_best().get_fitness()), file=sys.stderr)
            self.logger.info('Generation: {:2}: Chromosome Size: {}, Partial Fitness: {:3}'.format(i, len(ch), population.get_best().get_fitness()))
            
            # Generation: 1600: Best Fitness: 770.5590142921287
            # population.print_best()
            self.logger.info([ch])
            if population.population[0].chromosome == population.population[-1].chromosome:
                print('Converged. Breaking')
                break
        return population.population[0].chromosome
        
        
    def merge_partials(self):
        for partial in self.partials_population:
            assert len(partial) == len(set(partial))
        print(len(self.partials_population))
        while len(self.partials_population) > 1:
            [a, b] = self.iu.pick_merge(self.partials_population)
            a, b = max(a,b), min(a,b)       # ensure the higher index is being popped first
            p1 = self.partials_population.pop(a)
            p2 = self.partials_population.pop(b)
            # print('two news')
            # new = self.iu.merge(p1, p2)
            # print(new)
            # new = self.iu.merge(p1, p2)
            # print(new)
            
            # with 
            # print(self.config_string)
            # config = configparser.ConfigParser()
            # config.read_string(config_string)
            
            res = self.run_merged(p1, p2)
            assert len(res) == len(set(res))
            self.partials_population.append(res)
            try:
                assert len(set([item for sublist in self.partials_population for item in sublist])) == self.partials_size
            except AssertionError:
                print(p1)
                print(p2)
                print(res)
                raise AssertionError
            print(len(self.partials_population))
            print(self.partials_population)
        
        
