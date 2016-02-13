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
__author__ = 'norsd@163.com'
# 为matplotlib显示中文
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plot_node(a_node_text, a_center_pt, a_parent_pt, a_node_type):
    create_plot.ax1.annotate(a_node_text, xy=a_parent_pt, xycoords='axes fraction',
                            xytext=a_center_pt, textcoords='axes fraction',
                            va="center", ha="center", bbox=a_node_type, arrowprops=arrow_args)


def create_plot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_leafs_count(inTree))
    plot_tree.totalD = float(get_tree_depth(inTree))
    plot_tree.xOff = -0.5/plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(inTree, (0.5, 1.0), '')
    plt.show()


def get_leafs_count(a_my_tree: dict)->int:
    cnt = 0
    first_str = a_my_tree.keys()[0]
    second_dict = a_my_tree[first_str]
    for k in second_dict.keys():
        if type(second_dict[k]).__name__ == 'dict':
            cnt += get_leafs_count(second_dict[k])
        else:
            cnt += 1
    return cnt


def get_tree_depth(a_my_tree: dict)-> int:
    max_depth = 0
    first_str = a_my_tree.keys()[0]
    second_dict = a_my_tree[first_str]
    for k in second_dict.keys():
        if type(second_dict[k]) == type({}):
            this_depth = 1 + get_tree_depth(second_dict[k])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_mid_text(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    create_plot.ax1.text(xMid, yMid, txtString)


def plot_tree(myTree: dict, parentPt, nodeTxt):
    numLeafs = get_leafs_count(myTree)
    depth = get_tree_depth(myTree)
    firstStr = myTree.keys()[0]
    cntrPt = (plot_tree.xOff + (1.0 + float(numLeafs))/2.0/plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cntrPt, parentPt, nodeTxt)
    plot_node(firstStr, cntrPt, parentPt, decisionNode)
    second_dict = myTree[firstStr]
    plot_tree.yOff = plot_tree.yOff - 1.0/plot_tree.totalD
    for k in second_dict.keys():
        if type(second_dict[k]) == type({}):
            plot_tree(second_dict[k], cntrPt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0/plot_tree.totalW
            plot_node(second_dict[k], (plot_tree.xOff, plotTree.yOff), cntrPt, leafNode)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntrPt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0/plot_tree.totalD
    s
