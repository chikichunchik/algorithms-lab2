from DB_handler.DB import DB
import random

index_file_path = "C:/Users/andry/Desktop/kpi/2/algo/lab2/index.json"
main_file_path = "C:/Users/andry/Desktop/kpi/2/algo/lab2/main.json"
database = DB(index_file_path, main_file_path, is_new=True, expected_elements_number=6000)
for i in range(1000):
    database.add(random.randint(0, 10000))
for i in range(10000):
    database.set(i, 'a')
for i in range(10000):
    database.delete(i)