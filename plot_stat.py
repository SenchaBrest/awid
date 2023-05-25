import datetime
import os
import matplotlib.pyplot as plt

def plot(start_date, end_date):
    files = []
    path = 'runs/detect/track'
    for dirname in os.listdir(path):
        dir_path = os.path.join(path, dirname)
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                if start_date <= create_time <= end_date:
                    files.append(file_path)
    files = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    d = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.replace("\n", "").split(" ")
                cls = line[0]
                id = line[-1] if len(line) == 6 else None
                time = datetime.datetime.fromtimestamp(os.path.getctime(f))
                if not id:
                    continue
                if id in d:
                    d[id]["time"] = time - d[id]["time_in"]
                else:
                    d[id] = {"cls": cls, "time_in": time, "time": datetime.timedelta(seconds=0, microseconds=0)}
    person = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "0"]
    bicycle = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "1"]
    car = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "2"]
    motorcycle = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "3"]
    bus = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "5"]
    truck = [d[id]["time"].total_seconds() for id in d.keys() if d[id]["cls"] == "7"]

    _, axs = plt.subplots(nrows=2, ncols=3, figsize=(10, 6))
    axs[0, 0].hist(person, bins=20, color='blue', alpha=0.5)
    axs[0, 1].hist(bicycle, bins=20, color='orange', alpha=0.5)
    axs[0, 2].hist(car, bins=20, color='green', alpha=0.5)
    axs[1, 0].hist(motorcycle, bins=20, color='red', alpha=0.5)
    axs[1, 1].hist(bus, bins=20, color='purple', alpha=0.5)
    axs[1, 2].hist(truck, bins=20, color='pink', alpha=0.5)
    axs[0, 0].set_title('person')
    axs[0, 1].set_title('bicycle')
    axs[0, 2].set_title('car')
    axs[1, 0].set_title('motorcycle')
    axs[1, 1].set_title('bus')
    axs[1, 2].set_title('truck')
    plt.show()