# coding:utf-8
from numpy import *
import operator

__author__ = 'norsd@163.com'


def classify0(inx, data_set, labels, k):
    data_set_size = data_set.shape[0]
    # numpy.tile
    diff_mat = tile(inx, (data_set_size, 1)) - data_set



def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

