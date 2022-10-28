import string


class DataCalculation:
    def __init__(self, dataset: list):
        self.dataset = dataset

    def calculate_entropy(self):
        pass

    def get_probability(self, data_subset: list, key: string):
        temp_subset = []
        value_set = set()
        for data in data_subset:
            temp_subset.append(data[key])
            value_set.add(data[key])
        return [temp_subset.count(value)/len(temp_subset) for value in value_set]


