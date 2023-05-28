# import uuid

# # Генерация случайного уникального идентификатора
# unique_id = uuid.uuid4()

# print(unique_id)




# if __name__ == '__main__':
#     db = Database()
#     db.create_table()
#     #db.files2sql("https://s1.moidom-stream.ru/s/public/0000001301.m3u8")
#     print(db.get_records("0000001301.m3u8", datetime(2023, 5, 24, 10, 30), datetime(2023, 5, 29, 10, 30)))
    
#     db.close()


# import schedule
# import time

# def make_db(self, url):
#     schedule.every(1).minutes.do(self.db.files2sql, url)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)



# import glob

# files_path = "*.txt"
# output_file = "all.txt"
# files = glob.glob(files_path)

# with open(output_file, "w", encoding="utf-8") as outfile:
#     for f in files:
#         with open(f, "r", encoding="utf-8") as infile:
#             for line in infile:
#                 outfile.write(f"{f}\t{line}")