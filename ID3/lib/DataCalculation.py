import string
import math
from collections import defaultdict

class DataCalculation:
    def __init__(self, dataset: list):
        self.dataset = dataset
        self.entropy = self.calculate_entropy(dataset, "survived")
        print(self.entropy)

    @staticmethod
    def __calculate_entropy(data_subset: list, key: string = "survived"):
        occurrence = defaultdict(int)
        entropy = 0
        subset_size = len(data_subset)
        for data in data_subset:
            occurrence[data[key]] += 1
        for value in occurrence.values():
            prob = value / subset_size
            entropy -= prob * math.log(prob, 2)
        return entropy


    def get_probability(self, data_subset: list, key: string):
        temp_subset = []
        value_set = set()
        for data in data_subset:
            temp_subset.append(data[key])
            value_set.add(data[key])
        return [temp_subset.count(value)/len(temp_subset) for value in value_set]


