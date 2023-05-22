import tkinter as tk
import vlc
import subprocess     
import os
import datetime
import matplotlib.pyplot as plt

from plot_stat import plot

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Application")
        self.master.geometry('700x700')
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        self.start_button = tk.Button(self, text="Start", command=self.to_start)
        self.start_button.grid()
        self.to_forget = [self.start_button]


    def to_start(self):
        self.clear_actions()
        self.get_address()


    def get_address(self):
        self.address_label = tk.Label(self, text="Enter the address of the broadcast:", width=30, height=3)
        self.address_label.grid()
        self.address_entry = tk.Entry(self, width=30)
        self.address_entry.insert(0, "https://s1.moidom-stream.ru/s/public/0000001301.m3u8")
        self.address_entry.grid()
        self.ok_button = tk.Button(self, text="OK", command=self.to_work, width=30, height=30)
        self.ok_button.grid()

        self.to_forget = [
            self.address_label, 
            self.address_entry,
            self.ok_button
        ]


    def to_work(self):
        self.address = self.address_entry.get()

        self.to_make = [
            {"text": "Start broadcast", "command": self.start_broadcast},
            {"text": "Start analizer", "command": self.start_analizer},
            {"text": "Load stat", "command": self.time_picker},
            {"text": "Load critic", "command": self.load_critic},
            {"text": "Back", "command": self.back}
        ]
        self.clear_actions()
        self.show_actions()


    def clear_actions(self):
        for obj in self.to_forget: obj.grid_forget()
        self.to_forget.clear()


    def show_actions(self):
        for obj in self.to_make: 
            self.obj = tk.Button(self, text=obj["text"], command=obj["command"])
            self.to_forget.append(self.obj)
            self.obj.grid()


    def start_broadcast(self):
        self.to_make[0] = {"text": "Stop broadcast", "command": self.stop_broadcast}
        self.clear_actions()
        self.show_actions()

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.address)
        self.player.set_media(self.media)
        self.canvas = tk.Canvas(self.master)
        self.canvas.grid()
        self.player.set_hwnd(self.canvas.winfo_id())
        self.player.play()


    def stop_broadcast(self):
        self.to_make[0] = {"text": "Start broadcast", "command": self.start_broadcast}
        self.clear_actions()
        self.show_actions()
    
        self.player.stop()
        self.canvas.destroy()
        self.instance.release() 


    def start_analizer(self):
        self.to_make[1] = {"text": "Stop analizer", "command": self.stop_analizer}
        self.clear_actions()
        self.show_actions()
    
        command = [
            'yolo', 
            'track',
            'model=yolov8n.pt', 
            f'source={self.address}', 
            'device=None', 
            'show=False', 
            'save=False',
            'save_txt=True', 
            'tracker="bytetrack.yaml"',
        ]

        # self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.yolo = subprocess.Popen(command)


    def stop_analizer(self):
        self.to_make[1] = {"text": "Start analizer", "command": self.start_analizer}
        self.clear_actions()
        self.show_actions()
        
        # self.process.terminate()
        self.yolo.kill()


    def back(self):
        try:
            self.stop_broadcast()
        except:
            pass

        try:
            self.stop_analizer()
        except:
            pass

        self.clear_actions()
        self.to_make.clear()

        self.get_address()


    def label_entry(self, text, args1, args2):
        label = tk.Label(self.master, text=text)
        label.grid(row=args1[0], column=args1[1], padx=args1[2], pady=args1[3])
        entry = tk.Entry(self.master)
        entry.grid(row=args2[0], column=args2[1], padx=args2[2], pady=args2[3])
        return label, entry


    def time_picker(self):
        self.clear_actions()

        self.y1_label, self.y1_entry = self.label_entry(text="Год", args1=(1, 0, 5, 5), args2=(2, 0, 5, 5))
        self.m1_label, self.m1_entry = self.label_entry(text="Месяц", args1=(3, 0, 5, 5), args2=(4, 0, 5, 5))
        self.d1_label, self.d1_entry = self.label_entry(text="День", args1=(5, 0, 5, 5), args2=(6, 0, 5, 5))
        self.h1_label, self.h1_entry = self.label_entry(text="Час", args1=(7, 0, 5, 5), args2=(8, 0, 5, 5))
        self.min1_label, self.min1_entry = self.label_entry(text="Минута", args1=(9, 0, 5, 5), args2=(10, 0, 5, 5))

        self.y2_label, self.y2_entry = self.label_entry(text="Год", args1=(1, 1, 5, 5), args2=(2, 1, 5, 5))
        self.m2_label, self.m2_entry = self.label_entry(text="Месяц", args1=(3, 1, 5, 5), args2=(4, 1, 5, 5))
        self.d2_label, self.d2_entry = self.label_entry(text="День", args1=(5, 1, 5, 5), args2=(6, 1, 5, 5))
        self.h2_label, self.h2_entry = self.label_entry(text="Час", args1=(7, 1, 5, 5), args2=(8, 1, 5, 5))
        self.min2_label, self.min2_entry = self.label_entry(text="Минута", args1=(9, 1, 5, 5), args2=(10, 1, 5, 5))

        self.ok_button = tk.Button(self, text="OK", command=self.show_stat)#, width=30, height=30)
        self.ok_button.grid()
        
        self.to_forget = [
            self.y1_label, self.y1_entry,
            self.m1_label, self.m1_entry,
            self.d1_label, self.d1_entry,
            self.h1_label, self.h1_entry,
            self.min1_label, self.min1_entry,
            self.y2_label, self.y2_entry,
            self.m2_label, self.m2_entry,
            self.d2_label, self.d2_entry,
            self.h2_label, self.h2_entry,
            self.min2_label, self.min2_entry,
            self.ok_button
        ]


    def show_stat(self):
        self.y1 = self.y1_entry.get()
        self.y2 = self.y2_entry.get()
        self.m1 = self.m1_entry.get()
        self.m2 = self.m2_entry.get()
        self.d1 = self.d1_entry.get()
        self.d2 = self.d2_entry.get()
        self.h1 = self.h1_entry.get()
        self.h2 = self.h2_entry.get()
        self.min1 = self.min1_entry.get()
        self.min2 = self.min2_entry.get()

        start_date = datetime.datetime(int(self.y1), int(self.m1), int(self.d1), int(self.h1), int(self.min1))
        end_date = datetime.datetime(int(self.y2), int(self.m2), int(self.d2), int(self.h2), int(self.min2))
        plot(start_date, end_date)
    
    
    def load_critic(self):
        pass


root = tk.Tk()
app = App(master=root)
app.mainloop()
