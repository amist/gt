import os
import re
import json
import matplotlib.pyplot as plt

cities_folder = 'gt/examples'
# cities_file = 'cities_qatar.json'
cities_file = 'vlsi131.json'
    
if __name__ == '__main__':
    with open(os.path.join(cities_folder, cities_file), 'r') as f:
        cities = json.loads(f.read())
        plt.clf()
        for city in cities:
            x, y = cities[city]
            plt.plot(x, y, '.', color='b')
            plt.savefig(cities_file + '.png')
