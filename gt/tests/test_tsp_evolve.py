import sys
import time
import configparser
from gt.runner import Runner
from gt.examples.tsp_evolve import *

# plt.ion()

if __name__ == '__main__':
    config_file = os.path.join(os.getcwd(), 'tsp_evolve.config')
    
    config = configparser.ConfigParser()
    config.read(config_file)
    k = TSPEvolve(config=config)
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
