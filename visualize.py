import os
import matplotlib.pyplot as plt
from gt.examples.tsp import TSP

def visualize():
    # order = [0,33,34,36,31,27,28,24,22,25,26,23,20,15,13,2,4,3,5,6,7,8,9,12,11,19,18,17,16,1,10,14,21,29,30,32,35,37]
    order = [0,23,22,21,17,18,19,15,12,11,10,6,2,1,5,8,4,3,7,9,13,14,16,24,27,25,20,26,28]
    
    config_file = os.path.join(os.getcwd(), 'tsp.config')
    tsp = TSP(config_file=config_file)
    tsp.chromosome = [(c, o) for o, c in enumerate(order)]
    tsp.cities = {
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
    tsp.print()
    plt.show()


if __name__ == '__main__':
    visualize()