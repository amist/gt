import os
import re
import json
import matplotlib.pyplot as plt

cities_file = ''
# log_file = 'logs/mult_1600.log'
# log_file = 'logs/logfile_2017-10-03_22.19.55.491657.log'    # first YouTube example
log_files = [
            'logs/2nd_vlsi131/best.log',
            ]

def get_cities(log_file):
    cities_file = ''
    with open(log_file, 'r') as f:
        for line in f:
            if line.startswith('data_file = '):
                _, cities_file = line.split(' = ')
                cities_file = cities_file.rstrip()
                break
                
    if cities_file == '':
        return None
        
    with open(cities_file, 'r') as f:
        return json.loads(f.read())
        

def create_frame(cities, generation, fitness, chromosomes):
    plt.clf()
    if generation != -1:
        plt.suptitle('generation = {}, fitness = {:.2f}'.format(generation, fitness))
    else:
        plt.suptitle('')
    for city in cities:
        x, y = cities[city]
        plt.plot(x, y, '.', color='b')
    for chromosome in chromosomes:
        for i in range(1, len(chromosome)):
            x1, y1 = cities[chromosome[i-1]]
            x2, y2 = cities[chromosome[i]]
            plt.plot([x1, x2], [y1, y2], color='k')
        x1, y1 = cities[chromosome[0]]
        x2, y2 = cities[chromosome[-1]]
        plt.plot([x1, x2], [y1, y2], color='k')
    # plt.show(block=False)
    # plt.pause(interval=0.001)
    
    
def get_rows(log_file):
    rows = []
    generation = fitness = chromosomes = None
    prev_generation = -1
    prefix = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            # print(line)
            # skip the config info
            if not line.startswith('---'):
                continue
            else:
                break
                
        for line in f:
            # print(line)
            if line.startswith('Generation'):
                m = re.search('Generation:\W*(\d+): Best Fitness: (\d+.\d+)', line)
                if m:
                    generation = int(m.group(1))
                    fitness = float(m.group(2))
                    # print(generation, fitness)
                else:
                    m = re.search('Generation:\W*(\d+): Chromosome Size: (\d+), Partial Fitness: (\d+.\d+)', line)
                    if m:
                        generation = int(m.group(1))
                        if generation <= prev_generation:
                            prefix += 1
                        prev_generation = generation
                        fitness = float(m.group(3))
                        # print('partial', generation, fitness)
            elif line.startswith('[['):
                chromosomes = line
                m = re.search(r'(\[.*\])', line)
                if m:
                    chromosomes = json.loads(m.group(1))
                    chromosomes = [[str(x) for x in chromosome] for chromosome in chromosomes]
            elif line.startswith('['):
                chromosomes = line
                # m = re.search(r'(\[.*\])', line)
                # if m:
                try:
                    chromosome = json.loads(line)
                    chromosomes = [[str(x) for x in chromosome]]
                except json.decoder.JSONDecodeError:
                    chromosomes = None    # entry in ini
                
            # if generation is not None and fitness is not None and chromosomes is not None:
            generation = generation or -1
            fitness = fitness or -1
            if chromosomes is not None:
                rows.append((prefix, generation, fitness, chromosomes))
                generation = fitness = chromosomes = None
            # else:
                # print(line)
                
    return rows
                
    
    
def create_images(log_file):
    cities = get_cities(log_file)
    # print(cities)
    rows = get_rows(log_file)
    # print(rows)
    base_dir = 'log_animations'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    log_dir = log_file.split('/')[-1]
    log_dir = os.path.join(base_dir, log_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    total_rows = len(rows)
    for i, row in enumerate(rows):
        prefix, generation, fitness, chromosomes = row
        create_frame(cities, generation, fitness, chromosomes)
        plt.savefig(os.path.join(log_dir, '{:06d}.png'.format(i)))
        print('Finished {}/{}'.format(i+1, total_rows), end='       \r')
    
    
if __name__ == '__main__':
    for log_file in log_files:
        create_images(log_file)