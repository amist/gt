from gt.population import *
import os
import sys
import json
import configparser


class Runner(object):
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        self.debug = config.getboolean('runner', 'debug')
        self.generations_number = config.getint('runner', 'generations_number')
        self.population_type = config.get('population', 'type')
        self.output_mode = config.get('runner', 'output_mode')

        individual_path = config.get('individual', 'class')
        package_name, class_name = individual_path.rsplit('.', 1)
        m = __import__(package_name, globals(), locals(), class_name)
        individual = getattr(m, class_name)

        if self.population_type == 'SimplePopulation':
            self.population = SimplePopulation(individual=individual, config_file=config_file)
        elif self.population_type == 'TypesPopulation':
            self.population = TypesPopulation(individual=individual, config_file=config_file)
        elif self.population_type == 'TspPopulation':
            self.population = TspPopulation(individual=individual, config_file=config_file)

    def get_solution(self):
        json_output = {
            'generations': [],
            'solution': [],
            'fitness': -1
        }
        try:
            for i in range(self.generations_number):
                ret = self.population.process_generation()
                if self.debug:
                    print('Generation: {:2}: Best Fitness: {:3}'.format(i, self.population.get_best().get_fitness()), file=sys.stderr)
                    if self.output_mode == 'graphic' or self.output_mode == 'console':
                        self.population.get_best().print()
                    elif self.output_mode == 'json':
                        generation = [x.get_solution() for x in self.population.population]
                        json_output['generations'].append(generation)
                        
                if ret is not None:
                    if ret == 'convergence':
                        print('Population converged completely. Finishing', file=sys.stderr)
                    break
        except KeyboardInterrupt:
            print('Ending due to KeyboardInterrupt', file=sys.stderr)
            if self.output_mode == 'json':
                json_output['solution'] = self.population.get_best().get_solution()
                json_output['fitness'] = self.population.get_best().get_fitness()
                json.dump(json_output, sys.stdout)
        return self.population.get_best()
