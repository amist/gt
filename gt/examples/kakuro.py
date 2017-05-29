import os
import random
import configparser

class Kakuro(object):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'run.config'))
    debug = config.getboolean('runner', 'debug')
    mutation_prob = config.getint('individual', 'mutation_probability')
    
    def __init__(self):
        self.chromosome = [
                [[None, None, ], [23, None, ], [30, None, ], [None, None, ], [None, None, ], [27, None, ], [12, None, ], [16, None, ], ],
                [[None, 16, ], [0], [0], [None, None, ], [17, 24, ], [0], [0], [0], ],
                [[None, 17, ], [0], [0], [15, 29, ], [0], [0], [0], [0], ],
                [[None, 35, ], [0], [0], [0], [0], [0], [12, None, ], [None, None, ], ],
                [[None, None, ], [None, 7, ], [0], [0], [7, 8, ], [0], [0], [7, None, ], ],
                [[None, None, ], [11, None, ], [10, 16, ], [0], [0], [0], [0], [0], ],
                [[None, 21, ], [0], [0], [0], [0], [None, 5, ], [0], [0], ],
                [[None, 6, ], [0], [0], [0], [None, None, ], [None, 3, ], [0], [0], ],
            ]
        self.fitness = None


    def get_fitness(self):
        if self.fitness is None:
            self.fitness = 0
            lists = []
            new_list = []
            for row in self.chromosome:
                for cell in row:
                    if len(cell) == 2 and cell[1] is not None:
                        lists.append(new_list)
                        new_list = [cell[1]]
                    elif len(cell) == 1:
                        new_list.append(cell[0])

            for row in zip(*self.chromosome):
                for cell in row:
                    if len(cell) == 2 and cell[0] is not None:
                        lists.append(new_list)
                        new_list = [cell[0]]
                    elif len(cell) == 1:
                        new_list.append(cell[0])
            lists.append(new_list)
            lists = lists[1:]
            #print(lists)
            for l in lists:
                total = l[0]
                vals = l[1:]
                self.fitness += abs(total - sum(vals))
                self.fitness += 10 * (len(vals) - len(set(vals)))
        return self.fitness


    def get_child(self, other):
        child = Kakuro()
        partition = random.randint(0, len(self.chromosome)-1)
        child.chromosome = self.chromosome
        child.chromosome[partition:] = other.chromosome[partition:]
        return child


    def mutate(self, scope_data=None):
        if random.randrange(self.mutation_prob) == 0:
            #self.chromosome[random.randrange(len(self.chromosome))] = random.randint(1, 9)
            i = random.randrange(0, len(self.chromosome))
            j = random.randrange(0, len(self.chromosome))
            if len(self.chromosome[i][j]) == 1:
                self.chromosome[i][j] = [random.randint(1, 9)]


    def print(self):
        i = 0
        for row in self.chromosome:
            for cell in row:
                if type(cell) is list and len(cell) > 1:
                    print('XX' if cell[0] is None else '{:2d}'.format(cell[0]), end='')
                    print('\\', end='')
                    print('XX' if cell[1] is None else '{:2d}'.format(cell[1]), end='')
                else:
                    print(' {:2d}  '.format(cell[0]), end='')
                    i += 1
                print(' | ', end='')
            print()
        #print(['{:2d}'.format(x) for x in self.chromosome])
        print(self.get_fitness())
