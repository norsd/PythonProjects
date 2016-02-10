# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
from math import log
from typing import Tuple
from typing import List
from typing import TypeVar
import os
import operator
# 为matplotlib显示中文
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)


__author__ = 'norsd@163.com'


def calculate_shannon_ent(a_data_set):
    num_entries = len(a_data_set)
    label_counts = {} # 记录每种label出现的次数
    for feat_vec in a_data_set:
        current_label = feat_vec[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def split_set(a_data_set, a_axis, a_value):
    ret_data_set = []
    for feat_vec in a_data_set:
        if feat_vec[a_axis] == a_value:
            reduced_feat_vec = feat_vec[:a_axis]
            reduced_feat_vec.extend(feat_vec[a_axis+1:])
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set


def choose_best_feature_to_split(a_data_set: List):
    num_features = len(a_data_set[0]) -1
    base_entropy = calculate_shannon_ent(a_data_set)
    best_info_gain = 0.0; best_feature = -1
    for i in range(num_features):
        feat_list = [example[i] for example in a_data_set]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_set(a_data_set, i, value)
            prob = len(sub_data_set)/float(len(a_data_set))
            new_entropy += prob*calculate_shannon_ent(sub_data_set)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_count(a_class_list):
    class_count = {}
    for vote in a_class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.items, key = operator.itemgetter(1), reversed = True)
    return sorted_class_count[0][0]


def create_tree(a_data_set, a_labels):
    class_list = [example[-1] for example in a_data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    if len(a_data_set[0]) == 1:
        return majority_count(class_list)
    best_feat = choose_best_feature_to_split(a_data_set)
    best_feat_label = a_labels[best_feat]
    my_tree = { best_feat_label:{}}
    del(a_labels[best_feat])
    feat_values = [example[best_feat] for example in a_data_set]
    unique_vals = set(feat_values)
    for value in unique_vals:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = create_tree(split_set(a_data_set, best_feat, value), sub_labels)
    return my_tree

def test_create_set():
    data_set = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no'],
        [1, 1, 'maybe']
    ]
    return data_set