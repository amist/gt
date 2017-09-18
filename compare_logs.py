import os
import re
import matplotlib.pyplot as plt
from gt.examples.tsp import TSP

def get_xssyss(log):
    xss = []
    yss = []
    xs = []
    ys = []
    with open(log, 'r') as f:
        for line in f:
            if line.startswith('new run'):
                xss.append(xs)
                yss.append(ys)
                xs = []
                ys = []
            if line.startswith('Generation'):
                m = re.search('Generation:\W*(\d+): Best Fitness: (\d+.\d+)', line)
                if m:
                    xs.append(int(m.group(1)))
                    ys.append(float(m.group(2)))
                    
    xss.pop(0)
    yss.pop(0)
    return xss, yss
    

def visualize(logs):
    colors = ['r', 'b', 'g', 'k']
    for log, color in zip(logs, colors):
        xss, yss = get_xssyss(log)
        for xs, ys in zip(xss, yss):
            plt.plot(xs, ys, color=color)
        
    plt.show()
    
    
def stat_run(xs, ys):
    optimal = 27603
    for x, y in zip(xs, ys):
        if y < 1.01 * optimal:
            return x
    return None
    
    
def stats(logs):
    for i, log in enumerate(logs):
        total = 0
        success = 0
        failure = 0
        print('For log {} - {}'.format(i, log))
        xss, yss = get_xssyss(log)
        for xs, ys in zip(xss, yss):
            res = stat_run(xs, ys)
            if res is None:
                print('Did not reach approximation')
                failure += 1
            else:
                print('Reached 1 percent from optimal in {} generations'.format(res))
                success += 1
                total += res
        print('--> Succeeded {} out of {} tries with an average of {:.2f} generations'.format(success, success + failure, total / success))
    
    
def analyze(logs):
    stats(logs)
    visualize(logs)


if __name__ == '__main__':
    analyze([
        # '14-09-2017-10-51-55.60.log',
        # '14-09-2017-10-55-48.03.log',
        # '14-09-2017-11-38-08.26.log',
        # '14-09-2017-11-14-50.71.log',
        # '14-09-2017-11-41-09.22.log',
        # 'prob_2.log',
        # 'prob_2_dynamic_2.log',
        # 'prob_5_dynamic_2.log',
        'prob_5_dynamic_5.log',
        # 'prob_5_dynamic_5_inheritance.log',
        # '14-09-2017-13-11-30.26.log',
        # 'prob_5_dynamic_5_no_inheritance.log',
        # 'prob_5_dynamic_5_partial_inheritance.log',
        # 'prob_5_dynamic_5_partial_inheritance_better.log',
        # 'smart.log',
        # 'smart2.log',
        'prob_5_b.log',
        # 'prob_d_5.log',
        # 'prob_d_2.log',
        'diff_100.log',
        'weight_100.log',
        'unif_100.log',
        ])