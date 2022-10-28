import string
import csv
from itertools import islice


class DataReader:
    def __init__(self, path: string):
        self.path = path
        print(self.read_file())

    def read_file(self):
        with open(self.path) as file:
            batch = csv.reader(file, "excel", delimiter=",")
            next(batch)
            data = [{"class": int(row[1]), "name": row[2], "sex": row[3], "age": int(row[4]), "sib": int(row[5]),
                     "parch": int(row[6]), "survived": int(row[7])} for row in batch]
        return data

