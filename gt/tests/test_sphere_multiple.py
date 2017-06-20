import time
from gt.runner import Runner
from gt.examples.sphere import *

if __name__ == '__main__':
    for _ in range(10):
        runner = Runner(config_file='test.config')

        start_time = time.time()
        solution = runner.get_solution()
        end_time = time.time()
        print(solution.get_fitness())
    print('Running time: {} seconds'.format(end_time - start_time))
