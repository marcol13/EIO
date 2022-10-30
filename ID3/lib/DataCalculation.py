import string
import math
from collections import defaultdict

class DataCalculation:
    def __init__(self, dataset: list):
        self.dataset = dataset
        self.generate_tree(dataset)

        # output_key = "survived"
        # self.entropy = self.calculate_entropy(dataset, "survived")
        # print(self.entropy)

    def generate_tree(self, dataset: list, output_key: string = "survived"):
        dataset_size = len(dataset)
        global_entropy = self.__calculate_entropy(dataset)
        for key in dataset[0].keys():
            entropy_dict = {}
            if key == output_key:
                continue
            subset = self.__generate_subset(dataset, key)
            for (subset_key, subset_list) in subset.items():
                # print(subset_key)
                entropy, occurence = self.__calculate_entropy(subset_list)
                entropy_dict[subset_key] = {"entropy": entropy, "prob": occurence/dataset_size}
                # entropy_dict[subset_key]["prob"] =
                # print(entropy)
            conditional_entropy = self.__calculate_conditional_entropy(entropy_dict)
            gain = self.__calculate_gain(global_entropy[0], conditional_entropy)
            intrinsic_info = self.__calculate_intrinsic_info(entropy_dict)
            gain_ratio = self.__calculate_gain_ratio(gain, intrinsic_info)
            print(gain_ratio)
            # print(subset)

    def __delete_key(self, key: string):
        for element in self.dataset:
            element.pop(key, None)

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
        return entropy, sum(occurrence.values())

    @staticmethod
    def __calculate_conditional_entropy(entropy_dict: dict):
        entropy = 0
        for option in entropy_dict.values():
            entropy += option["entropy"] * option["prob"]
        return entropy

    @staticmethod
    def __calculate_gain(entropy: float, conditional_entropy: float):
        return entropy - conditional_entropy

    @staticmethod
    def __calculate_intrinsic_info(entropy_dict: dict):
        info = 0
        for option in entropy_dict.values():
            info -= option["prob"] * math.log(option["prob"], 2)
        return info

    @staticmethod
    def __calculate_gain_ratio(gain: float, intrinsic: float):
        return gain / intrinsic

    @staticmethod
    def __generate_subset(dataset: list, key: string):
        data_subset = defaultdict(list)
        for data in dataset:
            data_subset[data[key]].append(data)
        return data_subset

    def get_probability(self, data_subset: list, key: string):
        temp_subset = []
        value_set = set()
        for data in data_subset:
            temp_subset.append(data[key])
            value_set.add(data[key])
        return [temp_subset.count(value)/len(temp_subset) for value in value_set]


