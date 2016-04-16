
# coding:utf-8

import ML3.calculate
import ML3.trees
import ML3.treePlotter

__author__ = 'norsd@163.com'


data_set, property_names = ML3.trees.create_data_set()
entropy = ML3.calculate.calculate_shannon_entropy(data_set)
# print(entropy)

test_split = ML3.calculate.split_data_set(data_set, 0, 1)
# print(test_split)


test_best_split = ML3.calculate.choose_best_feather_split(data_set)
print(test_best_split)


fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = ML3.trees.create_tree(lenses, lensesLabels)
ML3.treePlotter.create_plot(lensesTree)