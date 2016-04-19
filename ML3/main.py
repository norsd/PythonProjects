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


fr = open('lenses.txt')
lenses = [tuple(inst.strip().split('\t')) for inst in fr.readlines()]
lensesLabels = ('age', 'prescript', 'astigmatic', 'tearRate')
lensesTree = ML3.calculate.create_decision_tree(lenses, lensesLabels)
# lensesTree = ML3.trees.create_tree(lenses, lensesLabels)
ML3.treePlotter.create_plot(lensesTree)