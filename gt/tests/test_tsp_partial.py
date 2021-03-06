import sys
import time
import random
import configparser
from gt.runner import Runner
from gt.examples.tsp_multiple import *
from gt.examples.tsp_partial import *
from gt.population import MergerPopulation
# import cProfile

# plt.ion()
config = None
config_string = ''
first_run = True

def run_once(start_point):
    global config, config_string, first_run
    # config_file = os.path.join(os.getcwd(), 'tsp_partial_{}.config'.format(start_point))
    config_file = os.path.join(os.getcwd(), 'tsp_partial_template.config')
    with open(config_file, 'r') as f:
        config_string = f.read()
        config_string = config_string.replace('START_POINT_PLACEHOLDER', 'start_point = {}'.format(start_point))
    # print(config_string)
    # exit()
    # config.read(config_file)
    config.read_string(config_string)
    
    # runner = Runner(config_file=config_file)
    runner = Runner(config_string=config_string, new_logfile=first_run)
    first_run = False
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
    global config, config_string, first_run
    
    config_file = os.path.join(os.getcwd(), 'tsp_partial_template.config')
    with open(config_file, 'r') as f:
        config_string = f.read()
        config_string = config_string.replace('START_POINT_PLACEHOLDER', 'start_point = {}'.format(0))
    config.read_string(config_string)
    
    data_file = config.get('problem', 'data_file')
    with open(data_file, 'r') as f:
        cities = json.loads(f.read())
        
    order_file = config.get('problem', 'order_file')
    with open(order_file, 'r') as f:
        order = json.loads(f.read())
    
    cities_number = max(map(int, cities.keys())) + 1
    sub_problem_size = config.getint('individual', 'size')
    # print(cities_number, sub_problem_size)
    weights = [3] * cities_number       # number of sub-problems each city has to be in
    starting_points = []
    while sum(weights) > 0:
        [start_point] = random.choices(range(cities_number), k=1, weights=weights)
        starting_points.append(start_point)
        start_point = str(start_point)
        # print(start_point)
        cities_in_sub_problem = [x[0] for x in order[start_point][:sub_problem_size]]
        # print(order[start_point][:sub_problem_size])
        # print(cities_in_sub_problem)
        for city in cities_in_sub_problem:
            if weights[city] > 0:
                weights[city] = weights[city] - 1
    # print(starting_points)
    # print(len(starting_points))
    # return
    solutions_collection = []
    for i, start_point in enumerate(starting_points):
        print('Run {} out of {}'.format(i+1, len(starting_points)+1))
        solution_chromosome = run_once(start_point)
        solutions_collection.append(solution_chromosome)
    
    # # # # for start_point in [53, 89, 74]:        # for missing points in vlsi131
    # for start_point in range(0, 131, 4):
        # solution_chromosome = run_once(start_point)
        # solutions_collection.append(solution_chromosome)
        
    # for start_point in [53, 89, 74]:        # for missing points in vlsi131
        # solution_chromosome = run_once(start_point)
        # solutions_collection.append(solution_chromosome)
    print(solutions_collection)
    
    # solutions_collection = [[124, 125, 0, 128, 129, 120, 119, 115, 127, 126], [8, 2, 3, 9, 10, 4, 11, 24, 23, 22], [9, 10, 22, 21, 20, 6, 7, 8, 2, 3], [16, 17, 18, 13, 5, 12, 1, 6, 14, 15], [18, 12, 6, 14, 15, 16, 17, 19, 26, 25], [29, 30, 31, 32, 33, 21, 20, 19, 27, 28], [24, 44, 43, 42, 41, 40, 39, 38, 23, 11], [30, 31, 20, 19, 25, 26, 27, 28, 46, 29], [48, 35, 34, 33, 21, 20, 29, 30, 31, 32], [38, 37, 36, 35, 34, 33, 21, 22, 23, 39], [39, 40, 41, 42, 43, 44, 24, 23, 37, 38], [41, 42, 60, 44, 43, 24, 23, 38, 39, 40], [49, 50, 56, 52, 51, 32, 31, 55, 47, 48], [57, 56, 52, 51, 50, 49, 48, 47, 35, 58], [50, 51, 52, 56, 57, 63, 66, 65, 62, 49], [59, 60, 61, 44, 43, 42, 41, 58, 72, 73], [78, 81, 55, 54, 46, 45, 64, 68, 75, 77], [55, 81, 78, 77, 75, 68, 64, 45, 46, 54], [71, 67, 63, 58, 59, 73, 72, 86, 80, 76], [67, 71, 76, 80, 79, 69, 65, 70, 66, 63], [83, 84, 85, 86, 80, 72, 67, 71, 76, 79], [67, 72, 80, 86, 85, 84, 83, 79, 76, 71], [92, 94, 87, 82, 81, 79, 83, 84, 85, 88], [84, 83, 82, 81, 87, 93, 99, 94, 92, 88], [111, 117, 110, 96, 95, 90, 91, 97, 104, 103], [114, 105, 106, 102, 101, 100, 98, 112, 121, 118], [97, 96, 111, 110, 116, 120, 117, 122, 103, 104], [106, 107, 113, 124, 126, 115, 109, 108, 99, 102], [114, 105, 106, 101, 100, 112, 123, 130, 121, 118], [122, 129, 128, 120, 116, 119, 115, 110, 111, 117], [119, 115, 110, 111, 117, 122, 129, 128, 120, 116], [113, 107, 106, 105, 114, 118, 121, 124, 125, 126], [120, 117, 122, 129, 128, 127, 126, 115, 119, 116], [89, 74, 53, 45, 46, 54, 64, 68, 75, 77]]       # first YouTube animation
    
    # for s in solutions_collection:
        # assert len(s) == len(set(s))
    # exit()
    # print_solution(cities, solutions_collection)
    # s = set(range(len(cities)))
    # for sol in solutions_collection:
        # s -= set(sol)
    # print(s)
    # import matplotlib.pyplot as plt;plt.show();exit()
    
    # print(cities)
    tp = TSPPartial()
    TSPPartial.cities = cities
    # tp.cities = cities
    
    mp = MergerPopulation(tp)
    for ch in solutions_collection:
        mp.partials_population.append(ch)
        
    mp.initialize_process(config_string)
    # while len(mp.partials_population) > 0:
    # while len(mp.partials_population) > 0 or mp.population[0] != mp.population[-1]:
        # mp.process_generation()
        # print_solution(tp.cities, [mp.population[0]])
        
    mp.merge_partials()
    
    if False:
        import matplotlib.pyplot as plt
        plt.show()
    
    unimportant = False     # unimportant stuff for final graphic output
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
        
        
def print_solution(cities, chromosomes):
    import matplotlib.pyplot as plt
    plt.clf()
    for chromosome in chromosomes:
        chromosome = [str(x) for x in chromosome]
        
        # plt.suptitle('fitness = {}'.format(self.get_fitness()))
        for city in cities:
            x, y = cities[city]
            plt.plot(x, y, '.', color='b')
        for i in range(len(chromosome)):
            x1, y1 = cities[chromosome[i-1]]
            x2, y2 = cities[chromosome[i]]
            plt.plot([x1, x2], [y1, y2], color='k')
        x1, y1 = cities[chromosome[0]]
        x2, y2 = cities[chromosome[-1]]
        plt.plot([x1, x2], [y1, y2], color='k')
        plt.show(block=False)
        plt.pause(interval=0.001)


if __name__ == '__main__':
    # cProfile.run('run()')
    for _ in range(20):
        config = configparser.ConfigParser()
        run()
        first_run = True