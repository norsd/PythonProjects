# coding:utf-8

from numpy import *
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar
from norlib.Dictionary import *

__auth__ = 'di_shen_sh@gmail.com'

T = TypeVar('T')


def calculate_native_bayes(a_data_set, a_labels):
    """
    计算每个单词属于特定label的概率
    @param a_data_set:
    datas = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
        ]
    @param a_labels:
    labels = [0, 1, 0, 1, 0, 1]
    @return:
    {
    0:{ dog: 0.8, mr: 0.2, ...}, 每个词属于label0的概率
    1:{},
    }
    """
    dt_ret = {}
    for i in range(0, len(a_labels)):
        dt_ret.setdefault(a_labels[i], {})

    # 每个词汇出现的个数
    # 例如:
    # { dog:{ label0: 2, label1: 5, label2: 5},
    #   cat:{ label0: 1, label1: 9, label2: 0},
    #   ......
    # }
    dt_count = {}
    dt_label_count = {}
    set_word = set([])
    set_label = set(a_labels)
    for i in range(0, len(a_data_set)):
        label = a_labels[i]
        row_data = a_data_set[i]
        set_word.update(row_data)
    for word in set_word:
        dt_count[word] = {}
        for label in set_label:
            dt_count[word][label] = 0
    for i in range(0, len(a_data_set)):
        label = a_labels[i]
        row_data = a_data_set[i]
        for data in row_data:
            dt_count[data]["all"] += 1
            dt_count[data][label] += 1

        dt_count.setdefault(label, 0)
        dt_count[label] += len(data)
        for w in data:
            dt = get_value(dt_ret, label, {})
            dt.setdefault(w, 0)
            dt[w] += 1
    for (k, v) in dt_root.items():
        dt = v
        label = k
        for (kw, vw) in dt.items():
            word = kw
            dt[word] /= float(dt_count[label])
    return tuple(dt_root.values())
