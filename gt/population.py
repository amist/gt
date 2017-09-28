import os
import sys
import json
import json
import configparser
import random


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
    def __init__(self, individual, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
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
                parent1, parent2 = random.choices(self.population, weights=fitnesses, k=2)
            elif self.expansion_type == 'different':
                k = 5
                candidates = random.choices(self.population, k=k)
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
            # if self.population[0].chromosome == self.population[-1].chromosome:
                # return 'convergence'
                
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

    def get_best(self):
        return self.population[0]


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

        
class TspPopulation(SimplePopulation):
    def __init__(self, individual, config_file='test.config'):
        SimplePopulation.__init__(self, individual=individual, config_file=config_file)
        
        
    def process_generation(self):
        ret = SimplePopulation.process_generation(self)
        if ret == 'convergence':
            print('population converged. working on mutations solely')
            for individual in self.population:
                self.mutation_prob = 0