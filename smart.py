import os
import matplotlib.pyplot as plt
from gt.examples.tsp import TSP

cities = {
 "0": [ 27462.5000 , 12992.2222 ],
 "1": [ 20833.3333 , 17100.0000 ],
 "2": [ 20900.0000 , 17066.6667 ],
 "3": [ 21300.0000 , 13016.6667 ],
 "4": [ 21600.0000 , 14150.0000 ],
 "5": [ 21600.0000 , 14966.6667 ],
 "6": [ 21600.0000 , 16500.0000 ],
 "7": [ 22183.3333 , 13133.3333 ],
 "8": [ 22583.3333 , 14300.0000 ],
 "9": [ 22683.3333 , 12716.6667 ],
"10": [ 23616.6667 , 15866.6667 ],
"11": [ 23700.0000 , 15933.3333 ],
"12": [ 23883.3333 , 14533.3333 ],
"13": [ 24166.6667 , 13250.0000 ],
"14": [ 25149.1667 , 12365.8333 ],
"15": [ 26133.3333 , 14500.0000 ],
"16": [ 26150.0000 , 10550.0000 ],
"17": [ 26283.3333 , 12766.6667 ],
"18": [ 26433.3333 , 13433.3333 ],
"19": [ 26550.0000 , 13850.0000 ],
"20": [ 26733.3333 , 11683.3333 ],
"21": [ 27026.1111 , 13051.9444 ],
"22": [ 27096.1111 , 13415.8333 ],
"23": [ 27153.6111 , 13203.3333 ],
"24": [ 27166.6667 , 9833.3333  ],
"25": [ 27233.3333 , 10450.0000 ],
"26": [ 27233.3333 , 11783.3333 ],
"27": [ 27266.6667 , 10383.3333 ],
"28": [ 27433.3333 , 12400.0000 ]
}
optimal_order = [0,23,22,21,17,18,19,15,12,11,10,6,2,1,5,8,4,3,7,9,13,14,16,24,27,25,20,26,28]

def d(chromosome, color='k'):
    chromosome = [str(x) for x in chromosome]
    global cities
    
    for city in cities:
        x, y = cities[city]
        plt.plot(x, y, '*', color='b')
    for i in range(1, len(cities)):
        x1, y1 = cities[chromosome[i-1]]
        x2, y2 = cities[chromosome[i]]
        # plt.arrow(x1, y1, x2-x1, y2-y1, head_width=0.05, head_length=0.1, fc='k', ec='k')
        plt.plot([x1, x2], [y1, y2], color=color)
    x1, y1 = cities[chromosome[0]]
    x2, y2 = cities[chromosome[len(cities)-1]]
    plt.plot([x1, x2], [y1, y2], color='y')
    plt.show(block=False)
    plt.pause(interval=0.001)

def cross():
    global cities
    global optimal_order
    config_file = os.path.join(os.getcwd(), 'tsp.config')
    
    t1 = TSP(config_file=config_file)
    t1.chromosome = [0,23,22,21,17,18,19,15,12,11,10,6,2,1,5,8,4,3,7,9,16,14,13,24,27,26,20,25,28]
    # d(t1.chromosome, color='r')
    
    
    t2 = TSP(config_file=config_file)
    # t2.chromosome = [0,23,22,17,21,18,19,12,11,10,15,6,2,1,5,8,4,3,7,9,13,14,16,24,27,25,20,26,28]
    t2.chromosome = [0,28,26,20,25,27,24,16,14,13,9,7,3,4,8,5,1,2,6,15,10,11,12,19,18,21,17,22,23]
    # d(t2.chromosome, color='b')
    
    child = t1.get_child(t2)
    print(child.chromosome)
    print(optimal_order)
    d(child.chromosome, color='g')
    
    plt.show()


if __name__ == '__main__':
    cross()