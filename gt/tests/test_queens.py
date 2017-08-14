import time
from gt.runner import Runner
from gt.examples.queens import *

if __name__ == '__main__':
    config_file = os.path.join(os.getcwd(), 'test.config')
    k = Queens(config_file=config_file)
    k.print()
    runner = Runner(config_file=config_file)
    # exit()
    
    start_time = time.time()
    solution = runner.get_solution()
    end_time = time.time()
    solution.print()
    print('Running time: {} seconds'.format(end_time - start_time))
    #for s in runner.population.population:
    #    print(s.get_fitness())
