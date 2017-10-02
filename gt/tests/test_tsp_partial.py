import sys
import time
import configparser
from gt.runner import Runner
from gt.examples.tsp_multiple import *
# import cProfile

# plt.ion()
config = configparser.ConfigParser()

def run_once(start_point):
    global config
    # config_file = os.path.join(os.getcwd(), 'tsp_partial_{}.config'.format(start_point))
    config_file = os.path.join(os.getcwd(), 'tsp_partial_template.config'.format(start_point))
    with open(config_file, 'r') as f:
        config_string = f.read()
        config_string = config_string.replace('START_POINT_PLACEHOLDER', 'start_point = {}'.format(start_point))
    # print(config_string)
    # exit()
    # config.read(config_file)
    config.read_string(config_string)
    
    # runner = Runner(config_file=config_file)
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
        
    return solution.chromosome
        
        
def run():
    global config
    
    solutions_collection = []
    for start_point in range(0, 131, 10):
        solution_chromosome = run_once(start_point)
        solutions_collection.append(solution_chromosome)
    print(solutions_collection)
    # print('in main run')
    # print(solution_chromosome)
    
    unimportant = False     # unimportant stuff final graphic output
    if unimportant:
        data_file = config.get('problem', 'data_file')
        with open(data_file, 'r') as f:
            cities = json.loads(f.read())
            
        order_file = config.get('problem', 'order_file')
        with open(order_file, 'r') as f:
            order = json.loads(f.read())
            
        const_data = {
            'cities': cities,
            'order': order,
            'start_point': '0',     # meaningless here
        }
        # agruments are meaningless here
        k = TSPMultiple(config=config, start_point_ratio=0, const_data=const_data)
        # k.print()
        if k.output_mode == 'graphic':
            import matplotlib.pyplot as plt
            plt.show()
            
        #for s in runner.population.population:
        #    print(s.get_fitness())


if __name__ == '__main__':
    # cProfile.run('run()')
    run()