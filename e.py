import tkinter as tk
import vlc

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Application")
        self.master.geometry('700x700')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.get_address
        self.start_button.pack(anchor="center")

    def get_address(self):
        self.start_button.pack_forget()
        self.address_label = tk.Label(self, text="Enter the address of the broadcast:",
                                      width=30, height=3)
        self.address_label.pack()
        self.address_entry = tk.Entry(self, 
                                      width=30)
        self.address_entry.insert(0, "https://s1.moidom-stream.ru/s/public/0000001301.m3u8")
        self.address_entry.pack()
        self.ok_button = tk.Button(self, text="OK", command=self.save_address,
                                   width=30, height=30)
        self.ok_button.pack()

    def save_address(self):
        self.address = self.address_entry.get()
        self.to_make = [{"text": "Start broadcast", "command": self.start_broadcast},
                        {"text": "Start analizer", "command": self.start_analizer},
                        {"text": "Action 3", "command": self.plug}]
        self.to_forget=[self.address_label, 
                       self.address_entry,
                       self.ok_button]

        self.show_actions()

    def show_actions(self):
        for obj in self.to_forget: obj.pack_forget()
        self.to_forget.clear()
        # self.address_label.pack_forget()
        # self.address_entry.pack_forget()
        # self.ok_button.pack_forget()
        for obj in self.to_make: 
            self.obj = tk.Button(self, text=obj["text"], command=obj["command"])
            self.to_forget.append(self.obj)
            self.obj.pack(side="left")
        # self.start_obsrv_button = tk.Button(self, text="Start broadcast", command=self.start_broadcast)
        # self.action2_button = tk.Button(self, text="Start analizer", command=self.start_analizer)
        # self.action2_button.pack(side="left")
        # self.action3_button = tk.Button(self, text="Action 3")
        # self.action3_button.pack(side="left")

    # to_forget = [self.start_broadcast, self.start_analizer]
    # to_make_button = [{"text":},]
    def plug(self):
        pass
    
    def start_broadcast(self):


        self.to_make = [{"text": "Stop broadcast", "command": self.stop_broadcast},
                        {"text": "Start analizer", "command": self.start_analizer},
                        {"text": "Action 3", "command": self.plug}]
        self.show_actions()
        # for obj in self.to_forget: obj.pack_forget()
        # self.to_forget.clear()
        # # self.start_obsrv_button.pack_forget()
        # # self.action2_button.pack_forget()
        # # self.action3_button.pack_forget()

        # self.stop_obsrv_button = tk.Button(self, text="Stop broadcast", command=self.stop_broadcast)
        # self.stop_obsrv_button.pack(side="left")
        # self.action2_button = tk.Button(self, text="Action 2")
        # self.action2_button.pack(side="left")
        # self.action3_button = tk.Button(self, text="Action 3")
        # self.action3_button.pack(side="left")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.address)
        self.player.set_media(self.media)
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.player.set_hwnd(self.canvas.winfo_id())
        self.player.play()

    def stop_broadcast(self):


        self.to_make = [{"text": "Start broadcast", "command": self.start_broadcast},
                        {"text": "Start analizer", "command": self.start_analizer},
                        {"text": "Action 3", "command": self.plug}]

        self.show_actions()

        # self.stop_obsrv_button.pack_forget()
        # self.action2_button.pack_forget()
        # self.action3_button.pack_forget()

        # self.start_obsrv_button = tk.Button(self, text="Start broadcast", command=self.start_broadcast)
        # self.start_obsrv_button.pack(side="left")
        # self.action2_button = tk.Button(self, text="Action 2")
        # self.action2_button.pack(side="left")
        # self.action3_button = tk.Button(self, text="Action 3")
        # self.action3_button.pack(side="left")
    
        self.player.stop()
        self.canvas.destroy()
        self.instance.release()

    def start_analizer(self):
        pass

    def stop_analizer(self):
        pass


root = tk.Tk()
app = App(master=root)
app.mainloop()
