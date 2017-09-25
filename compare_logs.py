import os
import re
# import matplotlib.pyplot as plt
from gt.examples.tsp import TSP

dataset = 'wsahara'
# dataset = 'djibouti'

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
    global dataset
    if dataset == 'wsahara':
        optimal = 27603
    elif dataset == 'djibouti':
        optimal = 6656
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
    # visualize(logs)


if __name__ == '__main__':
    if dataset == 'wsahara':
        analyze([
            # 'prob_5_dynamic_5.log',
            # 'prob_5_b.log',
            # 'unif_100.log',
            'weight_100.log',
            'diff_100.log',
            ])
    elif dataset == 'djibouti':
        analyze([
            'djib_unif_100.log',
            'djib_weight_100.log',
            'djib_diff_100.log',
            ])
        