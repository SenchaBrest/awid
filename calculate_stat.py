from termgraph import termgraph as tg
from db import Database

def calculate_stat(start, end, url):
    db = Database()
    class_durations = db.get_records(url.split('/')[-1], start, end)
    db.close()

    person = class_durations["0"]
    bicycle = class_durations["1"]
    car = class_durations["2"]
    motorcycle = class_durations["3"]
    bus = class_durations["5"]
    truck = class_durations["7"]

    return person, bicycle, car, motorcycle, bus, truck


def get_labels():
    return [*[f'{2 ** (i - 1) if i > 0 else 0} < t < {2 ** i}' for i in range(10 + 1)], f't > {2 ** 10}']


def get_data(start, end, url): 
    db = Database()
    clss = db.get_records(url.split('/')[-1], start, end)
    db.close()
   
    def sep(numbers):
        result = []
        ranges = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        for i in range(len(ranges) + 1):
            lower_bound = 0 if i == 0 else ranges[i-1]
            upper_bound = float('inf') if i == len(ranges) else ranges[i]
            result.append(len([num for num in numbers if lower_bound < num <= upper_bound]))
        return result
    
    data = []
    for p, b, c, m, B, t in zip(sep(clss[0]), sep(clss[1]), sep(clss[2]), sep(clss[3]), sep(clss[5]), sep(clss[7])):
        data.append([p, b, c, m, B, t])

    return data


def plot(labels, data, normal_data):
    len_categories = 6
    args = {'format': '{:<5.0f}', 'suffix': '', 'no_labels': False}
    colors = [91, 92, 93, 94, 95, 96]
    tg.print_categories(["person", "bicycle", "car", "motorcycle", "bus", "truck"], colors)
    tg.stacked_graph(labels, data, normal_data, len_categories, args, colors)


