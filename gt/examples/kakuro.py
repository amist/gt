import os
import random
import configparser

class Kakuro(object):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'run.config'))
    debug = config.getboolean('runner', 'debug')
    mutation_prob = config.getint('individual', 'mutation_probability')
    layout = [
                [[None, None, ], [23, None, ], [30, None, ], [None, None, ], [None, None, ], [27, None, ], [12, None, ], [16, None, ], ],
                [[None, 16, ], [], [], [None, None, ], [17, 24, ], [], [], [], ],
                [[None, 17, ], [], [], [15, 29, ], [], [], [], [], ],
                [[None, 35, ], [], [], [], [], [], [12, None, ], [None, None, ], ],
                [[None, None, ], [None, 7, ], [], [], [7, 8, ], [], [], [7, None, ], ],
                [[None, None, ], [11, None, ], [10, 16, ], [], [], [], [], [], ],
                [[None, 21, ], [], [], [], [], [None, 5, ], [], [], ],
                [[None, 6, ], [], [], [], [None, None, ], [None, 3, ], [], [], ],
            ]
    
    def __init__(self):
        cl = sum([1 for r in self.layout for x in r if x == []])
        self.chromosome = [0]*cl
        self.fitness = None


    def get_fitness(self):
        if self.fitness is None:
            self.fitness = 0
            lists = []
            new_list = []
            i = 0
            for row in self.layout:
                for cell in row:
                    if len(cell) == 2 and cell[1] is not None:
                        lists.append(new_list)
                        new_list = [cell[1]]
                    elif len(cell) == 0:
                        new_list.append(self.chromosome[i])
                        i += 1
            i = 0
            for row in zip(*self.layout):
                for cell in row:
                    if len(cell) == 2 and cell[0] is not None:
                        lists.append(new_list)
                        new_list = [cell[0]]
                    elif len(cell) == 0:
                        new_list.append(self.chromosome[i])
                        i += 1
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
            self.chromosome[random.randrange(len(self.chromosome))] = random.randint(1, 9)


    def print(self):
        i = 0
        for row in self.layout:
            for cell in row:
                if type(cell) is list and len(cell) > 1:
                    print('XX' if cell[0] is None else '{:2d}'.format(cell[0]), end='')
                    print('\\', end='')
                    print('XX' if cell[1] is None else '{:2d}'.format(cell[1]), end='')
                else:
                    print(' {:2d}  '.format(self.chromosome[i]), end='')
                    i += 1
                print(' | ', end='')
            print()
        #print(['{:2d}'.format(x) for x in self.chromosome])
        print(self.get_fitness())
