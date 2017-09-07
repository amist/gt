import os
import sys
import configparser
import random


class BasePopulation(object):
    def expand_population(self):
        for _ in range(self.expansion_factor * len(self.population)):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            child = parent1.get_child(parent2)
            self.population.append(child)
            
            
    def show_diversity_info(self):
        best_chromosome = self.population[0].chromosome
        worst_chromosome = self.population[-1].chromosome
        


class SimplePopulation(BasePopulation):
    def __init__(self, individual, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        self.size = config.getint('population', 'size')
        self.expansion_factor = config.getint('population', 'expansion_factor')
        self.population = [individual(config_file=config_file) for _ in range(self.size)]
        
    def reset_population(self):
        if self.population[0].chromosome_type == 'c':
            ...

    def process_generation(self):
        self.expand_population()

        # min_val = min([min([x for x in i.chromosome]) for i in self.population])
        # max_val = max([max([x for x in i.chromosome]) for i in self.population])
        scope_data = None
        # min_val = 1
        # max_val = 9
        # scope_data = {'min_val': min_val, 'max_val': max_val}
        # print(scope_data)
        list(map(lambda x: x.mutate(scope_data=scope_data), self.population))
        # [x.mutate() for x in self.population]
        self.population.sort(key=lambda x: x.get_fitness(), reverse=False)
        self.population = self.population[:self.size]
        if self.population[0].chromosome == self.population[-1].chromosome:
            return 'convergence'
            
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
