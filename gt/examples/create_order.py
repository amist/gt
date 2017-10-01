import math
import json

def get_cities(data_file):
    with open(data_file, 'r') as f:
        cities = json.loads(f.read())
        return cities
        
        
def get_order(cities, start_city):
    # print(cities)
    distances = []
    x0, y0 = cities[str(start_city)]
    for i in range(len(cities)):
        x1, y1 = cities[str(i)]
        distances.append((i, math.sqrt((x1 - x0) ** 2 + (y1- y0) ** 2)))
    distances.sort(key=lambda x: x[1])
    return [x[0] for x in distances]
    
    
def get_closest(cities, city):
    return get_order(cities, city)[0]
    

if __name__ == '__main__':
    advanced = True
    # data_file = 'cities_qatar.json'
    # data_file = 'cities_wsahara.json'
    # data_file = 'cities280.json'
    data_file = 'vlsi131.json'
    # start_point = 60
    cities = get_cities(data_file)
    output = {}
    for start_point in range(len(cities)):
        order = get_order(cities, start_point)
        
        if advanced:
            nexts = []
            for i, o in enumerate(order):
                if i == 0:
                    nexts.append(-1)
                    continue
                ns = get_order(cities, o)
                # print(o, ns)
                for n in ns:
                    if n in order[:i]:
                        nexts.append(n)
                        break
                
                # for n in ns:
                    # if n not in order[:i+1]:
                        # nexts.append(n)
                        # break
        
        # print(order)
        # print(nexts)
        # print(len(order))
        # print(len(nexts))
        
        l = [[a,b] for (a,b) in zip(order, nexts)]
        output[str(start_point)] = l
    # print(l)
    print(repr(output).replace("'", '"'))
    