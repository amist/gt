import os
import random
from gt.examples.tsp import TSP
import unittest.mock as mock
import matplotlib.pyplot as plt

def analyze():
    config_file = os.path.join(os.getcwd(), 'tsp.config')
    
    population = []
    
    for _ in range(1):
        k = TSP(config_file=config_file)
        population.append(k)
    
    for ind in population:
        for city in ind.cities:
            x, y = ind.cities[city]
            plt.plot(x, y, '*', color='b')
        for i in range(1, ind.size):
            x1, y1 = ind.cities[ind.city_index_by_order(i-1)]
            x2, y2 = ind.cities[ind.city_index_by_order(i)]
            # plt.arrow(x1, y1, x2-x1, y2-y1, head_width=0.05, head_length=0.1, fc='k', ec='k')
            plt.plot([x1, x2], [y1, y2], color='k')
        x1, y1 = ind.cities[ind.city_index_by_order(0)]
        x2, y2 = ind.cities[ind.city_index_by_order(ind.size-1)]
        r = random.random()
        plt.plot([x1+r, x2+r], [y1+r, y2+r], color='y')
        plt.show(block=False)
    
    plt.pause(0.1)
    plt.show()
    

if __name__ == '__main__':
    analyze()
    