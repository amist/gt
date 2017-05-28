import time
from gt.runner import Runner
from gt.examples.sphere import *

if __name__ == '__main__':
    runner = Runner(individual=Sphere, config_file='run.config')

    start_time = time.time()
    solution = runner.get_solution()
    end_time = time.time()
    solution.print()
    print('Running time: {} seconds'.format(end_time - start_time))
    #for s in runner.population.population:
    #    print(s.get_fitness())
