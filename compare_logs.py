import os
import re
# import matplotlib.pyplot as plt
from gt.examples.tsp import TSP
import scipy.stats

# dataset = 'wsahara'
# dataset = 'djibouti'
dataset = 'qatar'

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
    elif dataset == 'qatar':
        optimal = 9352
    for x, y in zip(xs, ys):
        if y < 1.1 * optimal:
            return x
    return None
    
    
def print_stats(samp1, samp2):
    s, p = scipy.stats.ttest_ind(samp1, samp2)
    if p > 0.05:
        print(f'No statistical significance. statistic={s}, pvalue={p}')
    else:
        res1 = sum(samp1)
        res2 = sum(samp2)
        if res1 > res2:
            print(f'First is more. statistic={s}, pvalue={p}')
        elif res1 < res2:
            print(f'Second is more. statistic={s}, pvalue={p}')
        else:
            print(f'Both are the same. statistic={s}, pvalue={p}')
    
    
def stats(logs):
    gens = []
    ress = []
    for i, log in enumerate(logs):
        gens.append([])
        ress.append([])
        
        total = 0
        success = 0
        failure = 0
        print('For log {} - {}'.format(i, log))
        xss, yss = get_xssyss(log)
        for xs, ys in zip(xss, yss):
            res = stat_run(xs, ys)
            if res is None:
                # print('Did not reach approximation')
                failure += 1
                ress[i].append(False)
            else:
                # print('Reached 1 percent from optimal in {} generations'.format(res))
                success += 1
                total += res
                gens[i].append(res)
                ress[i].append(True)
        print('--> Succeeded {} out of {} tries with an average of {:.2f} generations'.format(success, success + failure, total / success))
        
    print()
    print('== for success rate ==')
    print_stats(ress[0], ress[1])
    print('== for number of generations ==')
    print_stats(gens[0], gens[1])
    # print(scipy.stats.ttest_ind(gens[0], gens[1]))
    
    
def analyze(logs):
    stats(logs)
    # visualize(logs)


if __name__ == '__main__':
    if dataset == 'wsahara':
        analyze([
            # 'prob_5_dynamic_5.log',
            # 'prob_5_b.log',
            # 'unif_100.log',
            # 'diff.log',
            # 'wsahara_weight.log',
            # 'wsahara_diff.log',
            'weight_100.log',
            'diff_100.log',
            ])
    elif dataset == 'djibouti':
        analyze([
            # 'djib_unif_100.log',
            # 'djib_weight_100.log',
            # 'djib_diff_100.log',
            'djibouti_weight_20.log',
            'djibouti_diff_20.log',
            ])
        