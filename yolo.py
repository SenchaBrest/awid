import subprocess
import os

class Yolo():
    def __init__(self):
        self.sessions = {}

    
    def __del__(self):
        for session in self.sessions.values():
            # session.terminate()
            session.kill()
        self.sessions = {}


    def make_command(self, url):
        command = [
            'yolo', 
            'track',
            'model=yolov8n.pt', 
            f'source={url}', 
            'project=saves',
            f'name={url.split("/")[-1]}',
            'device=None', 
            'show=False', 
            'save=False',
            'save_txt=True', 
            'tracker="bytetrack.yaml"',
        ]
        return command


    # def start_session(self, url):
    #     devnull = open(os.devnull, 'w')
    #     try:
    #         # self.sessions[url] = subprocess.Popen(self.make_command(url), stdout=devnull, stderr=devnull)
    #         self.sessions[url] = subprocess.Popen(self.make_command(url))

    #         devnull.close()
    #         return True
    #     except subprocess.CalledProcessError:
    #         devnull.close()
    #         return False

    def start_session(self, url):
        devnull = open(os.devnull, 'w')
        process = subprocess.Popen(self.make_command(url), stdout=devnull, stderr=devnull)
        self.sessions[url] = process
        devnull.close()



    def stop_session(self, url):
        if url in self.sessions:
            # self.sessions[url].terminate()
            self.sessions[url].kill()
            del self.sessions[url]

