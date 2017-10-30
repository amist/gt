import sys
import time
import random
import re
import configparser
from gt.runner import Runner
from gt.examples.tsp_evolve import *
# import cProfile

# plt.ion()

def run():
    config_file = os.path.join(os.getcwd(), 'tsp_evolve.config')
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    data_file = config.get('problem', 'data_file')
    with open(data_file, 'r') as f:
        cities = json.loads(f.read())
        
    number_of_cities = len(cities)
    start_point = str(random.randint(0, number_of_cities-1))
    print('Starts from point', start_point)
        
    order_file = config.get('problem', 'order_file')
    with open(order_file, 'r') as f:
        order = json.loads(f.read())[start_point]
        
    const_data = {
        'cities': cities,
        'order': order,
        'start_point': start_point,
    }
    
    k = TSPEvolve(config=config)
    # k.print()
    
    with open(config_file, 'r') as f:
        config_string = f.read()
        p = re.compile(r'evolution_start = (\d+)')
        config_string = p.sub('evolution_start = {}'.format(start_point), config_string)
        
    runner = Runner(config_string=config_string)
    # plt.show()
    # exit()
    
    start_time = time.time()
    solution = runner.get_solution()
    end_time = time.time()
    solution.print()
    print(solution.chromosome)
    print('Running time: {} seconds'.format(end_time - start_time), file=sys.stderr)
    if len(set(solution.chromosome)) != len(solution.chromosome):
        print('Error in solution')
    
    if k.output_mode == 'graphic':
        import matplotlib.pyplot as plt
        plt.show()
    #for s in runner.population.population:
    #    print(s.get_fitness())


if __name__ == '__main__':
    # cProfile.run('run()')
    run()