import time
from gt.runner import Runner
from gt.examples.tsp import *

# plt.ion()

if __name__ == '__main__':
    config_file = os.path.join(os.getcwd(), 'tsp.config')
    k = TSP(config_file=config_file)
    k.print()
    runner = Runner(config_file=config_file)
    # plt.show()
    # exit()
    
    start_time = time.time()
    solution = runner.get_solution()
    end_time = time.time()
    solution.print()
    print('Running time: {} seconds'.format(end_time - start_time))
    
    if k.graphic_output:
        import matplotlib.pyplot as plt
        plt.show()
    #for s in runner.population.population:
    #    print(s.get_fitness())
