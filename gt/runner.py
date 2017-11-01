from gt.population import *
import os
import sys
import json
import configparser
import logging
import datetime

class Runner(object):
    def __init__(self, config_file=None, config_string=None, new_logfile=True):
        config = configparser.ConfigParser()
        if config_file is not None:
            config.read(config_file)
        else:
            config.read_string(config_string)
        
        self.logger = logging.getLogger('result')
        self.logger.setLevel(logging.DEBUG)
        if new_logfile:
            if len(self.logger.handlers) > 0:
                self.logger.handlers[0].stream.close()
                self.logger.removeHandler(self.logger.handlers[0])
            fileh = logging.FileHandler('logs/logfile_{}.log'.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', '.')))
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = logging.Formatter('%(message)s')
            fileh.setFormatter(formatter)
            self.logger.addHandler(fileh) 
        
        for section in config.sections():
            self.logger.debug('[{}]'.format(section))
            for (k, v) in config.items(section):
                self.logger.debug('{} = {}'.format(k, v))
        self.logger.debug('---')
        
        self.debug = config.getboolean('runner', 'debug')
        self.generations_number = config.getint('runner', 'generations_number')
        self.population_type = config.get('population', 'type')
        self.output_mode = config.get('runner', 'output_mode')

        individual_path = config.get('individual', 'class')
        package_name, class_name = individual_path.rsplit('.', 1)
        m = __import__(package_name, globals(), locals(), class_name)
        individual = getattr(m, class_name)

        if config_file is not None:
            if self.population_type == 'SimplePopulation':
                self.population = SimplePopulation(individual=individual, config_file=config_file)
            elif self.population_type == 'TypesPopulation':
                self.population = TypesPopulation(individual=individual, config_file=config_file)
            elif self.population_type == 'TspPopulation':
                self.population = TspPopulation(individual=individual, config_file=config_file)
        else:
            if self.population_type == 'SimplePopulation':
                self.population = SimplePopulation(individual=individual, config_string=config_string)
            elif self.population_type == 'TypesPopulation':
                self.population = TypesPopulation(individual=individual, config_string=config_string)
            elif self.population_type == 'TspPopulation':
                self.population = TspPopulation(individual=individual, config_string=config_string)

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
                    if self.population.evolution_type == 'simple':
                        print('Generation: {:2}: Best Fitness: {:3}'.format(i, self.population.get_best().get_fitness()), file=sys.stderr)
                    elif self.population.evolution_type == 'progressive':
                        if self.population.ch_expansion_finished:
                            print('Generation: {:2}: Best Fitness: {:3}'.format(i, self.population.get_best().get_fitness()), file=sys.stderr)
                            self.logger.info('Generation: {:2}: Best Fitness: {:3}'.format(i, self.population.get_best().get_fitness()))
                        else:
                            print('Generation: {:2}: Chromosome Size: {}, Partial Fitness: {:3}'.format(i, self.population.get_best().size, self.population.get_best().get_fitness()), file=sys.stderr)
                            self.logger.info('Generation: {:2}: Chromosome Size: {}, Partial Fitness: {:3}'.format(i, self.population.get_best().size, self.population.get_best().get_fitness()))
                    if self.output_mode == 'graphic' or self.output_mode == 'console':
                        self.population.print_best()
                        # self.population.get_best().print()
                        # self.logger.info(self.population.get_best().chromosome)
                        self.logger.info(self.population.get_best_chromosome())
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
