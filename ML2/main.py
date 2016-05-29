# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
from typing import Tuple
from typing import List
from typing import TypeVar
from ML2.kNN import *
import os
import operator
import zipfile
# 为matplotlib显示中文
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)

__author__ = 'norsd@163.com'


if __name__ == '__main__':
    print("绘画3个不同样本分类图")
    run_draw_dating()

    print('''
测试文件datingTestSet.txt中的数据
拿文件中10%的数据作为待测数据
剩余90%作为已知样本
计算10%的数据的最后归类与实际10%数据的类别比较
打印出这10%的数据计算类别的准确率
    ''')
    dating_class_test()

    print("测试手写识别")
    number_recognize("MyNumbers/2.txt", 3)

