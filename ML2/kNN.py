# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
import os
import operator
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)


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


# 文件格式如下:
# #
# 40920	8.326976	0.953952	largeDoses
# 14488	7.153469	1.673904	smallDoses
# 26052	1.441871	0.805124	didntLike
# #
# 每项内容分别为: 飞行常客里程数, 玩视屏游戏消耗时间, 每周消费冰淇淋公升数，关注度
def file_to_matrix(a_filename):
    """
    将一个特定格式文件转化为2个matrix
    @param a_filename:
    @return:
    """
    fr = open(a_filename)
    f_lines = fr.readlines()
    f_length = len(f_lines)
    ret_mat = zeros((f_length, 3))
    # 将"largeDoses", "smallDoses", "didntLike"映射为数字
    dt_label = {}
    # 记录已经转化为数字的label的list
    vt_label = []
    index = 0
    for line in f_lines:
        line = line.strip()
        sub_lines = line.split('\t')
        # 只记录前3项数据,分别为:飞行常客里程数, 玩视屏游戏消耗时间, 每周消费冰淇淋公升数
        ret_mat[index, :] = sub_lines[0:3]
        label = sub_lines[-1]
        set_value(dt_label, label, len(dt_label)+1)
        vt_label.append(dt_label[label])
        index += 1
    ret_descs = dt_label.keys()
    return ret_mat, vt_label, ret_descs


# 添加data到dictionary中当key尚未存在时
def set_value(self, key, data):
    if key not in self:
        self[key] = data
    return


# 快速运行函数
def run_helper():
    import os
    os.chdir('C:\\GitHubRepositories\\PythonProjects\\ML2')
    a, b, desc = file_to_matrix("datingTestSet.txt")
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.xlabel("测试", fontproperties=font)
    plt.ylabel("ABC")
    ax = fig.add_subplot(111)
    # 下面的语句快速绘画数据点
    # labels存储了每种数据（例如"飞行常客里程数")对应的非0整数
    # 对每个label*15得到形状
    # 对每个label*15得到颜色
    # 缺点是无法分类
    # ax.scatter(a[:, 0], a[:, 1], 15.0*array(b), 15.0*array(b))
    xs = [v for (i, v) in enumerate(a[:, 0]) if b[i] == 1]
    ys = [v for (i, v) in enumerate(a[:, 1]) if b[i] == 1]
    ax.scatter(xs, ys, 15, "red")
    #ax.legend((teat, ), ("red", "green"))

    plt.show()


if __name__ == '__main__':
    run_helper()