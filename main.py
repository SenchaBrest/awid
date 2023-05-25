import click
from art import tprint
from simple_term_menu import TerminalMenu
import sys
from yolo import Yolo
from datetime import datetime
from calculate_stat import calculate_stat, get_labels, get_data, plot
import numpy as np
from termgraph import termgraph as tg


class App:
    def __init__(self):
        tprint("awid")

        self.yolo = Yolo()
        self.machine = {"start" : self.yolo.start_session, "stop" : self.yolo.stop_session}

        self.main_options = ["Url actions", "Analizer", "Get statistics", "Get videos", "Exit"]
        self.options = self.main_options

        self.urls = {}
        self.actions = {
            "Url actions" : self.url_actions,
            "Add url" : self.add_url, 
            "Edit url" : self.edit_url, 
            "Delete url" : self.delete_url, 
            "Analizer" : self.analizer,
            "Start analizer(s)" : self.start_analizer,
            "Stop analizer(s)" : self.stop_analizer,
            "Get statistics" : self.get_stat,
            "Get videos" : self.get_videos,
            "Exit" : self.exit
        }


    def url_actions(self):
        self.options = ["Add url", "Edit url", "Delete url", "Back"]
        self.update_menu()
        if self.menu.chosen_menu_entry == "Back":
            self.main()
        else:
            self.actions[self.menu.chosen_menu_entry]()


    def add_url(self):
        self.urls[input("Please, enter address: ")] = "not running"
        input("Press Enter to continue...")
        self.clear_console(2)
        self.url_actions()
 

    def edit_url(self):
        if len(self.urls) != 0:
            self.options = [*self.urls, "Back"]
            self.update_menu()
            if self.menu.chosen_menu_entry != "Back":
                if self.urls[self.menu.chosen_menu_entry] == "running":
                    print("Stop analizer for this url first, then try to edit it again.")
                    input("Press Enter to continue...")
                    self.clear_console(2)
                    self.edit_url()
                else:
                    url = input("Please, enter address: ")
                    if url != self.menu.chosen_menu_entry:
                        self.urls[url] = "not running"
                        del self.urls[self.menu.chosen_menu_entry]
                    input("Press Enter to continue...")
                    self.clear_console(2)
                    self.edit_url()
            else:
                self.url_actions()
        else:
            print("No urls to edit.")
            input("Press Enter to continue...")
            self.clear_console(2)
            self.url_actions()

    
    def delete_url(self):
        if len(self.urls) != 0:
            self.options = [*self.urls, "Back"]
            self.update_menu()
            if self.menu.chosen_menu_entry != "Back":
                if self.urls[self.menu.chosen_menu_entry] == "running":
                    print("Stop analizer for this url first, then try to edit it again.")
                    input("Press Enter to continue...")
                    self.clear_console(2)
                    self.delete_url()
                else:
                    answer = input("Are you sure you want to delete this url? [y/n]: ") or "n"
                    if answer.lower() == "y":
                        del self.urls[self.menu.chosen_menu_entry]
                        print("URL deleted.")
                    elif answer.lower() == "n":
                        print("Deletion cancelled.")
                    else:
                        print("Invalid key. Try again.")
                    input("Press Enter to continue...")
                    self.clear_console(3)
                    self.delete_url()
            else:
                self.url_actions()
        else:
            print("No urls to delete.")
            input("Press Enter to continue...")
            self.clear_console(2)
            self.url_actions()

    
    def analizer(self):
        self.options = ["Start analizer(s)", "Stop analizer(s)", "Back"]
        self.update_menu()
        if self.menu.chosen_menu_entry == "Back":
            self.main()
        else:
            self.actions[self.menu.chosen_menu_entry]()


    def start_analizer(self):
        if len(self.urls) != 0:
            self.options = [*[url + f"[{self.urls[url]}]"for url in self.urls.keys()], "Back"]
            self.update_menu()
            choice = self.menu.chosen_menu_entry.replace("[running]", "").replace("[not running]", "")
            if choice != "Back":
                if self.urls[choice] == "not running":
                    self.urls[choice] = "running"
                    self.machine["start"](choice)
                    print(f"Analizer for {choice} is running now.")
                else:
                    print("Analizer is already running.")
                input("Press Enter to continue...")
                self.clear_console(2)
                self.start_analizer()
            else:
                self.analizer()
        else:
            print("No analizers to start.")
            input("Press Enter to continue...")
            self.clear_console(2)
            self.main()


    def stop_analizer(self):
        if len(self.urls) != 0:
            self.options = [*[url + f"[{self.urls[url]}]"for url in self.urls.keys()], "Back"]
            self.update_menu()
            choice = self.menu.chosen_menu_entry.replace("[running]", "").replace("[not running]", "")
            if choice != "Back":
                if self.urls[choice] == "running":
                    self.urls[choice] = "not running"
                    self.machine["stop"](choice)
                    print(f"Analizer for {choice} is stopped.")
                else:
                    print("Analizer is already not running.")
                input("Press Enter to continue...")
                self.clear_console(2)
                self.stop_analizer()
            else:
                self.analizer()
        else:
            print("No analizers to start.")
            input("Press Enter to continue...")
            self.clear_console(2)
            self.main()


    def get_stat(self):
        if len(self.urls) != 0:
            self.options = [*self.urls, "Back"]
            self.update_menu()
            if self.menu.chosen_menu_entry != "Back":
                print("The time from which you want to display statistics:")
                date_from = self.get_datetime_from_input()
                print("The time until which you want to display statistics:")
                date_until = self.get_datetime_from_input()
                input("Press Enter to continue...")
                self.clear_console(5)

                labels = get_labels()
                data = get_data(*calculate_stat(date_from, date_until, self.menu.chosen_menu_entry.split('/')[-1]))
                plot(labels, data, tg.normalize(np.log1p(data), 25))
                
                input("Press Enter to continue...")
                self.clear_console(16)
                self.get_stat()
            else:
                self.main()
        else:
            print("No urls to get statistic.")
            input("Press Enter to continue...")
            self.clear_console(2)
            self.url_actions()


    def get_datetime_from_input(self):
        while True:
            try:
                datetime_str = input('Enter date and time in YYYY-MM-DD HH:MM format: ')
                selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                return selected_datetime
            except ValueError:
                input('Invalid date or time format. Press enter to continue.')
                self.clear_console(2)


    def get_videos(self):
        pass


    def exit(self):
        self.clear_console(7)
        sys.exit()
    

    def update_menu(self):
        self.menu = TerminalMenu(self.options)
        self.menu.show()


    def clear_console(self, n):
        for _ in range(n):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[J") 
            sys.stdout.flush()


    def main(self):
        self.options = self.main_options
        self.update_menu()
        self.actions[self.menu.chosen_menu_entry]()



if __name__ == "__main__":
    a = App()
    # a.start()
    a.main()