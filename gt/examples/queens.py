import os
import random
import configparser

class Queens(object):
    config = configparser.ConfigParser()
    # config.read(os.path.join(os.getcwd(), 'test.config'), encoding='utf8')
    # with open(os.path.join(os.getcwd(), 'test.config'), 'r') as f:
        # for line in f.readlines():
            # print(line)
    # print(os.path.join(os.getcwd(), 'test.config'))
    # debug = config.getboolean('runner', 'debug')
    # size = config.getint('individual', 'size')
    # mutation_prob = config.getint('individual', 'mutation_probability')
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config.read(config_file)
        self.size = self.config.getint('individual', 'size')
        self.mutation_prob = self.config.getint('individual', 'mutation_probability')
        
        self.chromosome = [random.randint(0, self.size-1) for _ in range(self.size)]
        self.fitness = None
        self.collisions = set()


    def get_fitness(self):
        if self.fitness is None:
            cols = set()
            r_diag = set()
            l_diag = set()
            for i, g in enumerate(self.chromosome):
                if g in cols or g - i in r_diag or g + i in l_diag:
                    # print(g)
                    self.collisions.add(i)
                cols.add(g)
                r_diag.add(g - i)
                l_diag.add(g + i)
            self.fitness = len(self.collisions)
        return self.fitness


    def get_child(self, other):
        child = Queens(config_file=self.config_file)
        partition = random.randint(0, len(self.chromosome)-1)
        child.chromosome = self.chromosome
        child.chromosome[partition:] = other.chromosome[partition:]
        return child


    def mutate(self, scope_data=None):
        pass


    def print(self):
        print(['{}'.format(x) for x in self.chromosome])
        print(self.get_fitness())
        
        rows_sep = '-{}'.format('--' * self.size)
        print(rows_sep)
        for i in range(self.size):
            row = [' ' if x != self.chromosome[i] else ('O' if i not in self.collisions else 'X') for x in range(self.size)]
            # row = '|{}'.format(' |' * self.size)
            # row[2 * self.chromosome[i] + 1] = '*'
            print('|{}|'.format('|'.join(row)))
            print(rows_sep)
        
