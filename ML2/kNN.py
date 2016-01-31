# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
import os
import operator
import zipfile
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)


__author__ = 'norsd@163.com'


def classify0(inx, data_set, labels, k):
    """
    [data0, data1, ...]
    与
    {
    [data0, data1, ...]
    [data0, data1, ...]
    ...
    }
    分别计算index.data0 与data_set.data0s的距离
    分别计算index.data1 与data_set.data1s的距离
    @param inx: 一个没有分类的一行数据集合[data0, data1, ...],
                    data0 表示一种特性0的量化值(例如：每年飞机里程数),
                    data1 表示一种特性1的量化值(例如: 每年玩游戏的小时数),
                    data2 ........
                    我们希望根据所有参数,最后函数告诉我们这个数据集合可以被认为符合哪一个label
                    注意应该对每一个特性的量化值事先做好归一化
    @param data_set:一个已经分类的多行数据集合
                    {
                        [data0, data1, ...]  <---0行
                        [data0, data1, ...]  <---1行
                        ...
                    }
                    已经分类的含义是，对于i行的数据，其中的
                    data_set[i]: [data0, data1, ...]
                    他的分类值为 labels[i]
                    例如 labels[i] == 3
                    3也许表示"非常喜欢"或者其他值
    @param labels:data_set的每一行数据的分类结果,每一个数字表示一个分类
                    [
                        1,
                        15,
                        82,
                        ...
                    ]
    @param k:从data_set中选取与inx距离最小的k个点
    @return:返回根据data_set预测inx属于哪一个分类
    """
    data_set_size = data_set.shape[0]
    # 将inx [data0, data1, ...]
    # 复制为
    # {
    #     [data0, data1, ...]
    #     [data0, data1, ...]
    #     ...
    # }
    # 行数与data_set_size一致
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
    ret_descs = dt_label
    return ret_mat, vt_label, ret_descs, ["飞行常客里程数", "玩视屏游戏消耗时间", "每周消费冰淇淋公升数"]


# 添加data到dictionary中当key尚未存在时
def set_value(self, key, data):
    if key not in self:
        self[key] = data
    return


def auto_norm(set_data):
    min_value = set_data.min()
    max_value = set_data.max()
    ranges = max_value - min_value
    set_norm = zeros(shape(set_data))
    m = set_data.shape[0]
    set_norm = set_data - tile(min_value, (m, 1))
    return set_norm, ranges, min_value


#
def dating_class_test():
    hot_ratio = 0.1
    mat_dating, vt_labels, c, d = file_to_matrix("datingTestSet.txt")
    mat_norm, ranges, min_values = auto_norm(mat_dating)
    m = mat_norm.shape[0]
    num_test_vecs = int(m*hot_ratio)
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classify0(mat_norm[i, :], mat_norm[num_test_vecs:m, :], vt_labels[num_test_vecs:m], 3)
        print("the classifier came back with: %d, the reaql answer is: %d", classifier_result, vt_labels[i])
        if classifier_result != vt_labels[i] :
            error_count += 1.0
    print("The total error rate is: %f", error_count/float(num_test_vecs))


def read_zip(a_relative_path):
    z = zipfile.ZipFile("digits.zip", "r")
    print(z.namelist())


# 快速运行函数
def run_helper():
    import os
    os.chdir('C:\\GitHubRepositories\\PythonProjects\\ML2')
    a, label_numbers, dt_desc, columns = file_to_matrix("datingTestSet.txt")
    norm = auto_norm(a)
    print(norm)
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # 下面的语句快速绘画数据点
    # labels存储了每种数据（例如"飞行常客里程数")对应的非0整数
    # 对每个label*15得到形状
    # 对每个label*15得到颜色
    # 缺点是无法分类
    # ax.scatter(a[:, 0], a[:, 1], 15.0*array(b), 15.0*array(b))
    hs = []
    xi = 0
    yi = 1
    for (desc, label_number) in dt_desc.items():
        xs = [v for (i, v) in enumerate(a[:, xi]) if label_numbers[i] == label_number]
        ys = [v for (i, v) in enumerate(a[:, yi]) if label_numbers[i] == label_number]
        scolor = "#{0:06X}".format(random.randint(0, 0xFFFFFF))
        h = ax.scatter(xs, ys, 15.0, color=scolor)
        hs.append((h,desc))
    ax.legend([h[0] for h in hs], [h[1] for h in hs])
    plt.xlabel(columns[xi], fontproperties=font)
    plt.ylabel(columns[yi], fontproperties=font)
    plt.show()


if __name__ == '__main__':
    run_helper()