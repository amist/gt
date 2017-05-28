import os
import random
import configparser

class Sphere(object):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'run.config'))
    debug = config.getboolean('runner', 'debug')
    size = config.getint('individual', 'size')
    mutation_prob = config.getint('individual', 'mutation_probability')
    
    def __init__(self):
        self.chromosome = [random.uniform(-1, 1) for _ in range(self.size)]
        self.fitness = None


    def get_fitness(self):
        if self.fitness is None:
            self.fitness = sum([x*x for x in self.chromosome])
        return self.fitness


    def get_child(self, other):
        child = Sphere()
        partition = random.randint(0, len(self.chromosome)-1)
        child.chromosome = self.chromosome
        child.chromosome[partition:] = other.chromosome[partition:]
        return child


    def mutate(self, scope_data=None):
        if scope_data is None:
            min_val = min(self.chromosome)
            max_val = max(self.chromosome)
        else:
            min_val = scope_data['min_val']# - 0.1
            max_val = scope_data['max_val']# + 0.1
        if random.randrange(self.mutation_prob) == 0:
            #print('m')
            if min_val == max_val:
                print('converged')
            else:
                scale = max_val - min_val
                min_range = min_val/scale - 0.1 * (max_val/scale - min_val/scale)
                max_range = max_val/scale + 0.1 * (min_val/scale - max_val/scale)
                if scale < 1:
                    self.chromosome[random.randrange(self.size)] = random.uniform(min_range, max_range)*scale


    def print(self):
        print(['{:.3f}'.format(x) for x in self.chromosome])
        print(self.get_fitness())
