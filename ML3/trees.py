# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
from math import log
from typing import Tuple
from typing import List
from typing import Dict
from typing import TypeVar
import os
import operator
# 为matplotlib显示中文
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)

__author__ = 'norsd@163.com'

os.chdir('C:\\GitHubRepositories\\PythonProjects\\ML3')


def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

