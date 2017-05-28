from gt.population import *
import os
import configparser

class Runner(object):
    def __init__(self, individual, config_file='run.config'):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), config_file))
        
        self.debug = config.getboolean('runner', 'debug')
        self.generations_number = config.getint('runner', 'generations_number')
        self.population_type = config.get('population', 'type')
        if self.population_type == 'SimplePopulation':
            self.population = SimplePopulation(individual=individual)

    def get_solution(self):
        for i in range(self.generations_number):
            self.population.process_generation()
            if self.debug:
                print('Generation: {}: Best Fitness: {}'.format(i, self.population.get_best().get_fitness()))
        return self.population.get_best()
