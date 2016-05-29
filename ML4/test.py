# coding:utf-8

from typing import List
from typing import Tuple
from typing import TypeVar
import ML4.calculate

__author__ = 'norsd@163.com'

T = TypeVar('T')


def create_data_set()->Tuple[List, List]:
    """
    返回2个数组
    1个含有6个子数组
    1个含有6个0或者1的长度为6的int[]
    数值0表示正常词汇
    数值1表示侮辱性词汇
    @return:
    """
    datas = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
        ]
    labels = [0, 1, 0, 1, 0, 1]
    return datas, labels

(data_set, labels) = create_data_set()
test = ML4.calculate.calculate_native_bayes(data_set, labels)

