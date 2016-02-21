
# coding:utf-8

import ML3.trees
import ML3.treePlotter

__author__ = 'norsd@163.com'


fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = ML3.trees.create_tree(lenses, lensesLabels)
ML3.treePlotter.create_plot(lensesTree)