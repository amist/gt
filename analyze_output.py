import os
import json
import matplotlib.pyplot as plt

def get_cities():
    with open(os.path.join('gt', 'examples', 'cities_djibouti.json'), 'r') as f:
        return json.load(f)
        
def get_data():
    with open('output.json', 'r') as f:
        return json.load(f)
        
def plot_generation(generation):
    cities = get_cities()
    # print(cities)
    # print(generation)
    for city in cities:
        x, y = cities[city]
        plt.plot(x, y, '*', color='b')
    
    size = len(cities)
    
    plt.figure(1)
    plt.clf()
    num = 9
    for j in range(num):
        for i in generation[j]:
            x1, y1 = cities[str((i-1)%size)]
            x2, y2 = cities[str(i)]
            plt.subplot('1{}{}'.format(num, j))
            plt.plot([x1, x2], [y1, y2], color='k')
        
    plt.show()

def analyze():
    data = get_data()
    for generation in data['generations']:
        # print(generation[0])
        plot_generation(generation)
    plot_generation(data['generations'][0])

if __name__ == '__main__':
    analyze()