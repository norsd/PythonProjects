# coding:utf-8
import ML3.calculate
import ML3.trees
import ML3.treePlotter
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar

T = TypeVar('T')

__author__ = 'di_shen_sh@163.com'


def create_data_set()-> Tuple[List[Tuple[int, int, str]], Tuple]:
    data_set = [
        (1, 1, 'maybe'),
        (1, 1, 'yes'),
        (1, 1, 'yes'),
        (1, 0, 'no'),
        (0, 1, 'no'),
        (0, 1, 'no'),
    ]
    labels = ('no surfacing', 'flippers')
    return data_set, labels


data_set, property_names = create_data_set()
entropy = ML3.calculate.calculate_shannon_entropy(data_set)
print(entropy)

test_split = ML3.calculate.split_data_set(data_set, 0, 1)
print(test_split)

test_best_split = ML3.calculate.choose_best_feather_split(data_set)
print(test_best_split)

dt = ML3.calculate.create_decision_tree(data_set, tuple(property_names))
print(dt)