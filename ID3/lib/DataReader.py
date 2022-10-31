import string
import csv


class DataReader:
    def __init__(self, path: string):
        self.path = path

    def read_file(self):
        with open(self.path) as file:
            batch = csv.reader(file, "excel", delimiter=",")
            next(batch)
            data = [{"class": int(row[1]), "sex": row[3], "age": self.__classify_age(int(row[4])), "sib": int(row[5]),
                     "parch": int(row[6]), "survived": "no" if int(row[7]) == 0 else "yes"} for row in batch]
        return data

    @staticmethod
    def __classify_age(age: int):
        if age <= 20:
            return "young"
        elif age < 40:
            return "middle"
        return "old"

