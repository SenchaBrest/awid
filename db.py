import sqlite3
import os
from datetime import datetime as dt

class Database():
    def __init__(self, name='data.db'):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

    
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass


    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                i INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                time TEXT,
                cls INTEGER,
                id TEXT
            )
        ''')

    def insert_record(self, name, time, cls, id):
        self.cursor.execute('''
            INSERT INTO records (name, time, cls, id)
            VALUES (?, ?, ?, ?)
        ''', (name, time, cls, id))
        self.conn.commit()  


    def get_records_ids(self, name, start_time, end_time):
        self.cursor.execute('''
            SELECT DISTINCT id FROM records
            WHERE name = ? AND julianday(time) BETWEEN julianday(?) AND julianday(?)
        ''', (name, start_time, end_time))
        return self.cursor.fetchall()

    def get_records(self, name, start_time, end_time):
        clss = {0: [], 1: [], 2: [], 3: [], 5: [], 7: []}
        self.cursor.execute('''
            SELECT DISTINCT id FROM records
            WHERE name = ? AND julianday(time) BETWEEN julianday(?) AND julianday(?)
        ''', (name, start_time, end_time))
        for id in  self.cursor.fetchall():
            self.cursor.execute('''
                SELECT time, cls FROM records
                WHERE name = ? AND id = ? AND julianday(time) BETWEEN julianday(?) AND julianday(?)
            ''', (name, *id, start_time, end_time))
            d1id = self.cursor.fetchall()
            format = '%Y-%m-%d %H:%M:%S.%f'

            if d1id[0][1] in clss.keys():
                clss[d1id[0][1]].append((dt.strptime(d1id[-1][0], format) - dt.strptime(d1id[0][0], format)).total_seconds())

        return clss
   
    
    def files2sql(self, url, unique_id, process):
        name = url.split('/')[-1]
        path = f"saves/{name}/labels/"

        while True:
            for filename in sorted(os.listdir(path), key=lambda x: int(x.split('_')[-1].split('.')[0])):
                file = os.path.join(path, filename)
                with open(file, "r", encoding="utf-8") as f:
                    for l in f:
                        l = l.replace("\n", "").split(" ")
                        id = l[-1] if len(l) == 6 else None
                        if id is not None:
                            self.insert_record(
                                name, 
                                dt.fromtimestamp(os.path.getctime(file)),
                                l[0],
                                f"{id}-{unique_id}"
                            )
                        else:
                            continue
                os.unlink(file)


        


    
if __name__ == '__main__':
    db = Database()
    db.create_table()
    #db.files2sql("https://s1.moidom-stream.ru/s/public/0000001301.m3u8")
    print(db.get_records_ids("0000001301.m3u8", dt(2023, 5, 28, 13, 30), dt(2023, 5, 28, 13, 30, 10)))
    
    db.close()
                                                   