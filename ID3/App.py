from lib.DataReader import DataReader
from lib.DataCalculation import DataCalculation

data = DataReader("./assets/titanic-homework.csv")
file = data.read_file()

calc = DataCalculation(file)
