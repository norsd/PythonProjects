# coding:utf-8
from numpy import *
import operator

__author__ = 'norsd@163.com'


def classify0(inx, data_set, labels, k):
    data_set_size = data_set.shape[0]
    # numpy.tile
    diff_mat = tile(inx, (data_set_size, 1)) - data_set
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    sorted_dist_indicies = sq_distances.argsort()
    class_count = {}
    for i in range(k):
        vote_i_label = labels[sorted_dist_indicies[i]]
        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def file_to_matrix(a_filename):
    fr = open(a_filename)
    f_lines = fr.readlines()
    f_length = len(f_lines)
    ret_mat = zeros((f_length, 3))
    class_label_vector = []
    index = 0
    dt_label = {}
    for line in f_lines:
        line = line.strip()
        sub_lines = line.split('\t')
        ret_mat[index, :] = sub_lines[0:3]
        set_value(dt_label, sub_lines[-1], len(dt_label))
        class_label_vector.append(dt_label[sub_lines[-1]])
        index += 1
    return ret_mat, class_label_vector


def set_value(self, key, data):
    if key not in self:
        self[key] = data
    return
