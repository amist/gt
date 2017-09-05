from gt.population import *
import os
import configparser


class Runner(object):
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        self.debug = config.getboolean('runner', 'debug')
        self.generations_number = config.getint('runner', 'generations_number')
        self.population_type = config.get('population', 'type')

        individual_path = config.get('individual', 'class')
        package_name, class_name = individual_path.rsplit('.', 1)
        m = __import__(package_name, globals(), locals(), class_name)
        individual = getattr(m, class_name)

        if self.population_type == 'SimplePopulation':
            self.population = SimplePopulation(individual=individual, config_file=config_file)
        if self.population_type == 'TypesPopulation':
            self.population = TypesPopulation(individual=individual, config_file=config_file)

    def get_solution(self):
        for i in range(self.generations_number):
            ret = self.population.process_generation()
            if self.debug:
                print('Generation: {:2}: Best Fitness: {:3}'.format(i, self.population.get_best().get_fitness()))
                self.population.get_best().print()
            if ret is not None:
                if ret == 'convergence':
                    print('Population converged completely. Finishing')
                break
        return self.population.get_best()
