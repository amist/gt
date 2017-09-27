import math
import json

def get_cities(data_file):
    with open(data_file, 'r') as f:
        cities = json.loads(f.read())
        return cities
        
        
def get_order(data_file, start_city):
    cities = get_cities(data_file)
    # print(cities)
    distances = []
    x0, y0 = cities[str(start_city)]
    for i in range(len(cities)):
        x1, y1 = cities[str(i)]
        distances.append((i, math.sqrt((x1 - x0) ** 2 + (y1- y0) ** 2)))
    distances.sort(key=lambda x: x[1])
    return [x[0] for x in distances]

if __name__ == '__main__':
    # data_file = 'cities_qatar.json'
    data_file = 'cities_wsahara.json'
    # data_file = 'cities280.json'
    order = get_order(data_file, 10)
    print(order)