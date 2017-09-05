import os
from gt.examples.tsp import TSP
import unittest.mock as mock

def comp(expected, actual):
    if expected == actual:
        print('OK')
    else:
        print('FAIL')

def test_crossover():
    config_file = os.path.join(os.getcwd(), 'tsp.config')
    k1 = TSP(config_file=config_file)
    k1.chromosome_type = 'b'
    k1.chromosome = [(0,0),(3,1),(2,2),(1,3)]
    k1.size = len(k1.chromosome)
    
    k2 = TSP(config_file=config_file)
    k2.chromosome_type = 'b'
    k2.chromosome = [(0,0),(1,1),(2,2),(3,3)]
    k2.size = len(k2.chromosome)
    
    for i in range(k1.size+1):
        with mock.patch('random.randint', lambda a,b: i):
            print('partition =', i)
            child = k1.get_child(k2)
            
            print('parent', k1.chromosome, end=' ')
            comp(k1.chromosome, [(0,0),(3,1),(2,2),(1,3)])
            print('parent', k2.chromosome, end=' ')
            comp(k2.chromosome, [(0,0),(1,1),(2,2),(3,3)])
            
            print('child', child.chromosome, end=' ')
            if i == 0:
                expected_chromosome = [(0,0),(1,1),(2,2),(3,3)]
            elif i == 1:
                expected_chromosome = [(0,0),(1,1),(2,2),(3,3)]
            elif i == 2:
                expected_chromosome = [(0,0),(3,1),(1,2),(2,3)]
            elif i == 3:
                expected_chromosome = [(0,0),(3,1),(2,2),(1,3)]
            elif i == 4:
                expected_chromosome = [(0,0),(3,1),(2,2),(1,3)]
            
            comp(child.chromosome, expected_chromosome)

if __name__ == '__main__':
    test_crossover()
    