import string
import math
from collections import defaultdict
from treelib import Tree
import uuid
from copy import deepcopy


class DataCalculation:
    def __init__(self, dataset: list):
        self.dataset = dataset
        self.__determine_threshold()
        self.tree = Tree()
        self.generate_tree(dataset)
        self.tree.show()

        # output_key = "survived"
        # self.entropy = self.calculate_entropy(dataset, "survived")
        # print(self.entropy)

    def generate_tree(self, dataset: list, output_key: string = "survived", parent_key: uuid.UUID = uuid.uuid4(),
                      parent_value: string = ""):
        dataset_size = len(dataset)
        global_entropy = self.__calculate_entropy(dataset)

        if global_entropy[0] == 0.0:
            parent_uuid = uuid.uuid4()
            self.tree.create_node(dataset[0][output_key], parent_uuid, parent=parent_key)
            return

        gain_ratio_dict = {}
        for key in dataset[0].keys():
            entropy_dict = {}
            if key == output_key:
                continue
            subset = self.__generate_subset(dataset, key)
            for (subset_key, subset_list) in subset.items():
                entropy, occurrence = self.__calculate_entropy(subset_list)
                entropy_dict[subset_key] = {"entropy": entropy, "prob": occurrence / dataset_size}
            conditional_entropy = self.__calculate_conditional_entropy(entropy_dict)
            gain = self.__calculate_gain(global_entropy[0], conditional_entropy)
            intrinsic_info = self.__calculate_intrinsic_info(entropy_dict)
            gain_ratio = self.__calculate_gain_ratio(gain, intrinsic_info)
            gain_ratio_dict[key] = gain_ratio
        if gain_ratio_dict == {}:
            return
        max_key, max_value = max(gain_ratio_dict.items(), key=lambda k: k[1])
        divided_dataset = self.__divide_dataset(dataset, max_key)

        for (key, data) in divided_dataset.items():
            node_uuid = uuid.uuid4()
            if self.tree.root is None:
                self.tree.create_node(max_key, parent_key)

            self.tree.create_node(f"{key} ({max_key})", node_uuid, parent=parent_key)
            self.generate_tree(data, parent_key=node_uuid, parent_value=str(key))

    def __determine_threshold(self, key: string = 'age', output_key: string = 'survived'):
        key_list = [tuple([data[key], 0 if data[output_key] == "no" else 1]) for data in self.dataset]
        key_list = sorted(key_list, key=lambda x: x[0])
        print(key_list)
        thresh_list = []
        counter = 1
        age_sum = key_list[0][1]
        for i in range(1, len(key_list) + 1):
            if key_list[i % len(key_list)][0] != key_list[i - 1][0]:
                thresh_list.append({"age": key_list[i - 1][0], "prob": age_sum / counter})
                counter = 1
                age_sum = key_list[i % len(key_list)][1]
            else:
                counter += 1
                age_sum += key_list[i % len(key_list)][1]

        max_gain_ratio = (0, 0)
        for i in range(0, len(thresh_list) - 1):
            if thresh_list[i]["prob"] != thresh_list[i + 1]["prob"]:
                thresh = (thresh_list[i]["age"] + thresh_list[i + 1]["age"]) / 2
                temp = (thresh, self.__check_threshold_gain(thresh))
                if max_gain_ratio[1] < temp[1]:
                    max_gain_ratio = temp

        self.__replace_values_by_thresh(max_gain_ratio[0])

    def __replace_values_by_thresh(self, threshold: float, key: string = "age"):
        for data in self.dataset:
            if data[key] <= threshold:
                data[key] = f"<= {threshold}"
            else:
                data[key] = f"> {threshold}"

    def __check_threshold_gain(self, threshold: float, key: string = "age"):
        dataset = deepcopy(self.dataset)
        entropy_dict = {}
        for data in dataset:
            data[key] = 0 if data[key] <= threshold else 1

        subset = self.__generate_subset(dataset, key)
        global_entropy = self.__calculate_entropy(dataset)
        for (subset_key, subset_list) in subset.items():
            entropy, occurrence = self.__calculate_entropy(subset_list)
            entropy_dict[subset_key] = {"entropy": entropy, "prob": occurrence / len(dataset)}
        conditional_entropy = self.__calculate_conditional_entropy(entropy_dict)
        gain = self.__calculate_gain(global_entropy[0], conditional_entropy)
        # intrinsic_info = self.__calculate_intrinsic_info(entropy_dict)
        # gain_ratio = self.__calculate_gain_ratio(gain, intrinsic_info)
        return gain

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
        return 0 if intrinsic == 0 else gain / intrinsic

    @staticmethod
    def __generate_subset(dataset: list, key: string):
        data_subset = defaultdict(list)
        for data in dataset:
            data_subset[data[key]].append(data)
        return data_subset

    @staticmethod
    def __divide_dataset(dataset: list, key: string):
        divided_dataset = defaultdict(list)
        for element in dataset:
            temp_key = element[key]
            element.pop(key, None)
            divided_dataset[temp_key].append(element)
        return divided_dataset

    def get_probability(self, data_subset: list, key: string):
        temp_subset = []
        value_set = set()
        for data in data_subset:
            temp_subset.append(data[key])
            value_set.add(data[key])
        return [temp_subset.count(value) / len(temp_subset) for value in value_set]
