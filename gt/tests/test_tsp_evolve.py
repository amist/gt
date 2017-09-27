import sys
import time
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
        
    order_file = config.get('problem', 'order_file')
    with open(order_file, 'r') as f:
        order = json.loads(f.read())
        
    const_data = {
        'cities': cities,
        'order': order,
    }
    
    k = TSPEvolve(config=config, const_data=const_data)
    # k.print()
    runner = Runner(config_file=config_file)
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