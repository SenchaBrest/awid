import subprocess
import os
from db import Database
import multiprocessing
import uuid


class Yolo():
    def __init__(self):
        self.sessions = {}
        self.db = Database()
        self.db.create_table()

    
    def __del__(self):
        for session in self.sessions.values():
            session.kill()
        self.sessions = {}
        self.db.close()


    def make_command(self, url):
        command = [
            'yolo', 
            'track',
            'model=yolov8n.pt', 
            f'source={url}', 
            'project=saves',
            f'name={url.split("/")[-1]}',
            'exist_ok=True',
            'device=None', 
            'show=False', 
            'save=False',
            'save_txt=True', 
            'tracker="bytetrack.yaml"',
        ]
        return command


    def start_session(self, url):
        devnull = open(os.devnull, 'w')
        process = subprocess.Popen(self.make_command(url), stdout=devnull, stderr=devnull)
        self.sessions[url] = process
        devnull.close()

        process_for_write_to_sql = multiprocessing.Process(target=self.db.files2sql, args=(url, uuid.uuid4(), self.sessions[url],))
        process_for_write_to_sql.start()
        self.sessions[f"{url}-files2sql"] = process_for_write_to_sql


    def stop_session(self, url):
        if url in self.sessions:
            self.sessions[url].kill()
            del self.sessions[url]
            self.sessions[f"{url}-files2sql"].terminate()
            del self.sessions[f"{url}-files2sql"]



