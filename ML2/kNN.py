# coding:utf-8
from matplotlib.font_manager import FontProperties
from numpy import *
import matplotlib.pyplot as plt
from typing import Tuple
from typing import List
from typing import TypeVar
import os
import operator
import zipfile
# 为matplotlib显示中文
font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)


__author__ = 'norsd@163.com'

# 定义泛型
T = TypeVar('T')


def classify0(inx: ndarray, data_set: ndarray, labels: List[T], k: int)-> T:
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


def auto_norm(set_data)-> Tuple[ndarray, float, float]:
    """
    把数据集归一
    @param set_data:
    @return:
    """
    min_value = set_data.min()
    max_value = set_data.max()
    ranges = max_value - min_value
    set_norm = zeros(shape(set_data))
    m = set_data.shape[0]
    set_norm = set_data - tile(min_value, (m, 1))
    return set_norm, ranges, min_value


def set_value(a_dict: dict, a_key, a_value)-> None:
    """
    当key尚未存在时,添加data到dictionary中
    @param a_dict:
    @param a_key:
    @param a_value:
    @return:
    """
    if a_key not in a_dict:
        a_dict[a_key] = a_value
    return


# region Dating Test Functions
def file_to_matrix(a_filename: str)-> Tuple[ndarray, list, dict, List[str]]:
    """
    将一个特定格式文件转化为matrix
                    40920	        8.326976	        0.953952	        largeDoses
                    14488	        7.153469	        1.673904	        smallDoses
                    26052	        1.441871	        0.805124	        didntLike
    每项内容分别为: 飞行常客里程数, 玩视屏游戏消耗时间, 每周消费冰淇淋公升数，关注度
    @param a_filename: 文件名
    @return:
        ret_mat     数行数据,举例第i行为[40920, 8.326976, 0.953952]，Columns分别表示"飞行常客里程数", "玩视屏游戏消耗时间", "每周消费冰淇淋公升数"
        vt_label    对每一行数据的一个分类,注意分类用数字表示，例如i行的数据类别为：LargeDoses, 在vt_label中的第i个就记录为1
        ret_descs   Dictionary<string,int> 用于转换类似 "LargeDoses"->1
        ["飞行常客里程数", "玩视屏游戏消耗时间", "每周消费冰淇淋公升数"]
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


def dating_class_test()-> None:
    """
    测试文件datingTestSet.txt中的数据
    拿文件中10%的数据作为待测数据
    剩余90%作为已知样本
    计算10%的数据的最后归类与实际10%数据的类别比较
    打印出这10%的数据计算类别的准确率
    """
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


def run_draw_dating():
    """
    快速运行函数
    绘画数据图
    @return:
    """
    """
    @return:
    """
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
# endregion


# region Number Recognize Functions
def extract_zip(a_target_dir: str)-> None:
    """
    解压digits.zip到a_path中
    @param a_target_dir:
    """
    z = zipfile.ZipFile("digits.zip", "r")
    name_list = z.namelist()
    for n in name_list:
        str_name = str(n)
        path = "{0}/{1}".format(a_target_dir, str_name)
        if str_name[-1] == '/':
            if not os.path.exists(path):
                os.mkdir(path)
        else:
            if not os.path.exists(path):
                bytes = z.read(str_name)
                f = open(path, 'wb')
                f.write(bytes)
                f.close()
            image_to_vector(path)


def image_to_vector(a_file_path)-> ndarray:
    """
    必须是32*32的图片
    @param a_file_path:
    @return:
    """
    f = open(a_file_path, 'r')
    lines = f.readlines()
    if len(lines) != 32:
        print("高度不合法的文件:", a_file_path)
        return
    vt = zeros((1, 32*32))
    for i in range(0, len(lines)):
        line = list(lines[i])[:32]
        if len(line) != 32:
            print("宽度({0})不合法的文件:{1}".format(len(line), a_file_path))
            return
        for j in range(0, 32):
            vt[0, i*32 + j] = line[j]
    return vt


def number_recognize(a_txt_path: str, a_k: int=3)-> None:
    os.chdir('C:\\GitHubRepositories\\PythonProjects\\ML2')
    extract_zip("c:/")
    traning_folder = "c:/trainingDigits"
    filenames = os.listdir(traning_folder)
    traning_matrix = zeros((len(filenames), 32*32))
    traning_labels = []
    for i in range(0, len(filenames)):
        filename = filenames[i]
        label = filename[0] # 文件名形如 4_129.txt 表示字符"4"的第129个样本
        vt = image_to_vector("{0}/{1}".format(traning_folder, filename))
        traning_matrix[ i,: ] = vt
        traning_labels.append(label)
    filename = a_txt_path
    vt = image_to_vector(filename)
    label_calculate = classify0(vt, traning_matrix, traning_labels, a_k)
    print("文件{0}是:{1}".format(a_txt_path, label_calculate))


def numbers_recognize():
    os.chdir('C:\\GitHubRepositories\\PythonProjects\\ML2')
    extract_zip("c:/")
    traning_folder = "c:/trainingDigits"
    filenames =  os.listdir(traning_folder)
    traning_matrix = zeros((len(filenames), 32*32))
    traning_labels = []
    for i in range(0, len(filenames)):
        filename = filenames[i]
        label = filename[0] # 文件名形如 4_129.txt 表示字符"4"的第129个样本
        vt = image_to_vector("{0}/{1}".format(traning_folder, filename))
        traning_matrix[ i,: ] = vt
        traning_labels.append(label)
    test_folder = "c:/testDigits"
    filenames = os.listdir(test_folder)
    error_count = 0
    for i in range(0, len(filenames)):
        filename = filenames[i]
        label_expected = filename[0] # 文件名形如 4_129.txt 表示字符"4"的第129个测试样本
        vt = image_to_vector("{0}/{1}".format(traning_folder, filename))
        label_calculate = classify0(vt, traning_matrix, traning_labels, 3)
        if label_expected != label_calculate:
            print("{0}被错认为是{1}".format(filename, label_calculate))
            error_count += 1
    print("Error count", error_count)
    print("错误率:{0}%".format(round(error_count*100/len(filenames), 2)))
# endregion


# region Obsolete functions
def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
# endregion


if __name__ == '__main__':
    # run_draw_dating()
    number_recognize("MyNumbers/2.txt", 3)

