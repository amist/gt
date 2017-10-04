import os
import json
import math
import matplotlib.pyplot as plt

def visualize():
    # chromosomes = [[31, 30, 29, 28, 25, 18, 13, 5, 12, 1, 6, 14, 15, 16, 17, 19, 26, 53, 45, 46, 54, 55, 47, 48, 49, 50, 51, 52, 56, 63, 67, 66, 62, 65, 69, 75, 68, 27, 20, 7, 8, 2, 3, 9, 10, 4, 11, 24, 41, 43, 44, 42, 61, 58, 57, 71, 86, 85, 84, 83, 88, 92, 94, 99, 108, 109, 110, 111, 96, 91, 90, 95, 97, 104, 103, 122, 117, 120, 129, 128, 116, 115, 119, 127, 126, 0, 125, 124, 105, 112, 123, 130, 121, 118, 114, 113, 107, 106, 102, 101, 100, 98, 93, 87, 78, 77, 64, 74, 89, 81, 82, 76, 70, 79, 80, 72, 73, 60, 59, 40, 23, 39, 38, 37, 36, 22, 21, 33, 32, 34, 35]]
    
    chromosomes = [[67, 63, 66, 70, 76, 71, 79, 83, 80, 86, 85, 84, 88, 92, 94, 87, 82, 81, 78, 77, 75, 68, 64, 45, 46, 54, 55, 69, 65, 56, 52, 51, 50, 49, 48, 47, 30, 29, 28, 27, 26, 25, 18, 12, 6, 14, 15, 16, 17, 19, 20, 31, 32, 33, 21, 34, 35, 22, 36, 37, 38, 23, 11, 24, 44, 43, 42, 41, 40, 39, 57, 58, 61, 60, 59, 73, 72]]
    chromosomes = [[110, 111, 117, 120, 96, 97, 95, 90, 91, 104, 103, 122, 129, 128, 116, 115, 119, 127, 126, 0, 125, 124, 121, 130, 123, 112, 100, 101, 102, 106, 107, 113, 114, 118, 105, 98, 93, 87, 78, 81, 82, 79, 76, 71, 80, 72, 73, 59, 58, 57, 56, 52, 51, 50, 49, 48, 47, 32, 21, 33, 34, 35, 22, 37, 38, 39, 23, 40, 41, 42, 60, 44, 43, 24, 11, 4, 10, 9, 3, 2, 8, 7, 20, 31, 30, 29, 28, 19, 17, 16, 15, 14, 6, 1, 12, 5, 13, 18, 25, 26, 27, 46, 45, 53, 74, 89, 77, 64, 68, 75, 54, 55, 62, 65, 66, 67, 63, 86, 85, 84, 83, 88, 92, 94, 99, 108, 109]]
    
    # didn't merged well
    chromosomes = [[67, 63, 66, 70, 76, 71, 79, 83, 80, 86, 85, 84, 88, 92, 94, 87, 82, 81, 78, 77, 75, 68, 64, 45, 46, 54, 55, 69, 65, 56, 52, 51, 50, 49, 48, 47, 30, 29, 28, 27, 26, 25, 18, 12, 6, 14, 15, 16, 17, 19, 20, 31, 32, 33, 21, 34, 35, 22, 36, 37, 38, 23, 11, 24, 44, 43, 42, 41, 40, 39, 57, 58, 61, 60, 59, 73, 72], [110, 111, 117, 120, 96, 97, 95, 90, 91, 104, 103, 122, 129, 128, 116, 115, 119, 127, 126, 0, 125, 124, 121, 130, 123, 112, 100, 101, 102, 106, 107, 113, 114, 118, 105, 98, 93, 87, 78, 81, 82, 79, 76, 71, 80, 72, 73, 59, 58, 57, 56, 52, 51, 50, 49, 48, 47, 32, 21, 33, 34, 35, 22, 37, 38, 39, 23, 40, 41, 42, 60, 44, 43, 24, 11, 4, 10, 9, 3, 2, 8, 7, 20, 31, 30, 29, 28, 19, 17, 16, 15, 14, 6, 1, 12, 5, 13, 18, 25, 26, 27, 46, 45, 53, 74, 89, 77, 64, 68, 75, 54, 55, 62, 65, 66, 67, 63, 86, 85, 84, 83, 88, 92, 94, 99, 108, 109]]
    
    chromosomes = [[110, 111, 117, 120, 96, 97, 95, 90, 91, 104, 103, 122, 129, 128, 116, 115, 119, 127, 126, 0, 125, 124, 121, 130, 123, 112, 100, 101, 102, 106, 107, 113, 114, 118, 105, 98, 93, 87, 78, 81, 82, 79, 76, 71, 80, 72, 73, 59, 61, 58, 57, 56, 52, 51, 50, 49, 48, 47, 32, 21, 33, 34, 35, 36, 22, 37, 38, 39, 23, 40, 41, 42, 60, 44, 43, 24, 11, 4, 10, 9, 3, 2, 8, 7, 20, 31, 30, 29, 28, 19, 17, 16, 15, 14, 6, 1, 12, 5, 13, 18, 25, 26, 27, 46, 45, 53, 74, 89, 77, 64, 68, 75, 54, 69, 55, 62, 65, 70, 66, 67, 63, 86, 85, 84, 83, 88, 92, 94, 99, 108, 109]]
    with open('gt/examples/vlsi131.json', 'r') as f:
        cities = json.loads(f.read())
    
        
    for city in cities:
        x, y = cities[city]
        plt.plot(x, y, '*', color='b')
        plt.text(x, y, city, color='r')
        
    print(len(set().union(*chromosomes)))
    for chromosome in chromosomes:
        print(len(chromosome))
        dist = 0
        for i in range(len(chromosome)):
            x1, y1 = cities[str(chromosome[i-1])]
            x2, y2 = cities[str(chromosome[i])]
            dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
        plt.suptitle('fitness = {}'.format(dist))
        chromosome = [str(x) for x in chromosome]
        for i in range(1, len(chromosome)):
            x1, y1 = cities[chromosome[i-1]]
            x2, y2 = cities[chromosome[i]]
            plt.plot([x1, x2], [y1, y2], color='k')
        x1, y1 = cities[chromosome[0]]
        x2, y2 = cities[chromosome[-1]]
        plt.plot([x1, x2], [y1, y2], color='k')
    
    plt.show()


if __name__ == '__main__':
    visualize()