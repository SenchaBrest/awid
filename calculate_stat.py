import os
import numpy as np
from termgraph import termgraph as tg
from datetime import datetime, timedelta

def calculate_stat(start, end, url):
    files = []
    path = f'saves/'

    needed = url.split('/')[-1]
    for dirname in os.listdir(path):
        if needed not in dirname:
            continue
        dir_path = os.path.join(path, dirname + "/labels")
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                create_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if start <= create_time <= end:
                    files.append(file_path)

    files = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    d = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.replace("\n", "").split(" ")

                id = line[-1] if len(line) == 6 else None
                if not id: continue

                cls = line[0]
                time = datetime.fromtimestamp(os.path.getctime(f))
                if id in d:
                    d[id]["time"] = time - d[id]["time_in"]
                else:
                    d[id] = {"cls": cls, "time_in": time, "time": timedelta(days=0, seconds=0, microseconds=0)}


    class_durations = {"0": [], "1": [], "2": [], "3": [], "5": [], "7": []}

    for id in d.keys():
        cls = d[id]["cls"]
        if cls in class_durations.keys(): 
            duration = d[id]["time"].total_seconds()
            class_durations[cls].append(duration)

    person = class_durations["0"]
    bicycle = class_durations["1"]
    car = class_durations["2"]
    motorcycle = class_durations["3"]
    bus = class_durations["5"]
    truck = class_durations["7"]

    return person, bicycle, car, motorcycle, bus, truck


def get_labels():
    return [*[f'{2 ** (i - 1) if i > 0 else 0} < t < {2 ** i}' for i in range(10 + 1)], f't > {2 ** 10}']


def get_data(person, bicycle, car, motorcycle, bus, truck):    
    def sep(numbers):
        result = []
        ranges = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        for i in range(len(ranges) + 1):
            lower_bound = 0 if i == 0 else ranges[i-1]
            upper_bound = float('inf') if i == len(ranges) else ranges[i]
            result.append(len([num for num in numbers if lower_bound < num <= upper_bound]))
        return result
    
    data = []
    for p, b, c, m, B, t in zip(sep(person), sep(bicycle), sep(car), sep(motorcycle), sep(bus), sep(truck)):
        data.append([p, b, c, m, B, t])

    return data


def plot(labels, data, normal_data):
    len_categories = 6
    args = {'format': '{:<5.0f}', 'suffix': '', 'no_labels': False}
    colors = [91, 92, 93, 94, 95, 96]
    tg.print_categories(["person", "bicycle", "car", "motorcycle", "bus", "truck"], colors)
    tg.stacked_graph(labels, data, normal_data, len_categories, args, colors)


if __name__ == "__main__":
    start = datetime(2023, 5, 1)
    end = datetime(2023, 5, 25)
    url = "https://s1.moidom-stream.ru/s/public/0000001301.m3u8"    

    labels = get_labels()
    data = get_data(*calculate_stat(start, end, url))
    
    plot(labels, data, tg.normalize(np.log1p(data),25))


