# coding:utf-8

from numpy import *
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar

__auth__ = 'di_shen_sh@gmail.com'


T = TypeVar('T')


def calculate_shannon_entropy(a_data_set: List[Tuple[int, int, str]]):
    """
    计算数据集的熵
    @param a_data_set:
        List[ Tuple[ int, int, ..., str] ]
        每一个Tuple[ int, int, ..., str]代表一个样本,
        每一个样本的各种属性的值分别被按固定顺序罗列在column: 0 到 -2
        例如属性分别为: 是否汪汪叫， 几只脚， 是否有胡须
        最后一个值为分类： 例如: 老虎，猫， 鸟
        计算∑p(xi)logp(xi)， p(xi)是指分类i的概率
    @return:
    """
    count = len(a_data_set)
    dt_kind = {}
    for item in a_data_set:
        last = item[-1]
        dt_kind[last] = dt_kind.get(last, 0) + 1
    sum_entropy = 0.0
    for key in dt_kind:
        value = float(dt_kind[key])
        probability = value/count
        log_probability = -math.log(probability, 2)
        sum_entropy += probability * log_probability
    return sum_entropy


def split_data_set(a_data_set: List[Tuple], a_property_index: int, a_value: int):
    """
    创建新的数据集
    从原数据集中剔除第i个属性, 且其此属性的值为 a_value
    @param a_data_set:
        原数据集,不做修改
    @param a_property_index:
        属性的序列号
    @param a_value:
        属性的值
    @return:
        [[1, 1, yes], [1, 1, yes], [1, 0, no], [0, 1, no], [0, 0, no]]
        split_data_set(datas, 0, 1)
        [[1, yes], [1, yes], [0, no]]
    """
    vt = []
    for item in a_data_set:
        axis_value = item[a_property_index]
        if axis_value == a_value:
            fore = item[:a_property_index]
            fore.extend(item[a_property_index + 1:])
            vt.append(fore)
    return vt


def get_property_count(a_data_set: List[Tuple]) -> int:
    """
    返回数据集属性的个数
    @param a_data_set:
    @return:
    """
    if len(a_data_set) == 0:
        return 0
    return len(a_data_set[0]) - 1


def get_property_values(a_data_set: List[Tuple], a_property_index: int) -> List[int]:
    """
    获取数据集中某一个属性的全部值
    @param a_data_set:
    @param a_property_index:
    @return:
    """
    dt = {}
    for item in a_data_set:
        property_value = item[a_property_index]
        dt[property_value] = 1
    return dt.keys()


def choose_best_feather_split(a_data_set: List[Tuple]) ->int:
    base_entropy = calculate_shannon_entropy(a_data_set)
    best_entropy_index = -1
    entropy_gain = 0.0
    count_split = get_property_count(a_data_set)
    for i in range(0, count_split):
        entropy = 0.0
        for current_split_value in get_property_values(a_data_set, i):
            sub_data_set = split_data_set(a_data_set, i, current_split_value)
            sub_entropy = calculate_shannon_entropy(sub_data_set)
            entropy += len(sub_data_set)/double(len(a_data_set))*sub_entropy
        print(entropy)
        if base_entropy - entropy > entropy_gain:
            entropy_gain = base_entropy - entropy
            best_entropy_index = i
    return best_entropy_index



