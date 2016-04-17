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


def remove_tuple_item(a_tuple: Tuple, a_index: int):
    vt = list(a_tuple)
    vt.pop(a_index)
    return tuple(vt)


def split_data_set(a_data_set: List[Tuple], a_property_index: int, a_property_value: int):
    """
    创建新的数据集
    从原数据集中剔除第i个属性, 且其此属性的值为 a_value
    @param a_data_set:
        原数据集,不做修改
    @param a_property_index:
        属性的序列号
    @param a_property_value:
        属性的值
    @return:
        [[1, 1, yes], [1, 1, yes], [1, 0, no], [0, 1, no], [0, 0, no]]
        split_data_set(datas, 0, 1)
        [[1, yes], [1, yes], [0, no]]
    """
    vt = []
    for t in a_data_set:
        value = t[a_property_index]
        if value == a_property_value:
            list_t = list(t)
            list_t.pop(a_property_index)
            vt.append(tuple(list_t))
    return vt


def split_data_set_to_dict(a_data_set: List[Tuple], a_property_index: int):
    """
    根据index个属性值返回dict<one_property_value, splitted_data_set>
    每一个key是第index个Property的一种可能值
    每一个value是第index个Property为key值时的 splitted_data_set
    @param a_data_set:
    @param a_property_index:
    @return:
    """
    dt = {}
    property_value = get_property_values(a_data_set, a_property_index)
    for v in property_value:
        dt[v] = []
    for t in a_data_set:
        dt[t[a_property_index]].append(remove_tuple_item(t, a_property_index))
    return dt


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
        if base_entropy - entropy > entropy_gain:
            entropy_gain = base_entropy - entropy
            best_entropy_index = i
    return best_entropy_index


def create_decision_tree(a_data_set: List[Tuple], a_property_names: Tuple):
    """
    @param a_data_set:
    @param a_property_names:
    @return:
    {"Fat":
        {
            {"yes" : "不受欢迎"},
            {"no"  :
                {
                    {"有钱" : "还收点欢迎"},
                    {"没钱" : "不受欢迎"}
                }
            }
        }
    },
    {"Cool": "受欢迎"}
    """
    if len(a_data_set) == 1:
        t = a_data_set[0]
        assert len(a_property_names) == 1, "fuck"
        p = a_property_names[0]
        return dict([p, t[-1]])
    elif len(a_property_names) == 0:
        raise "logical error"
    else:
        bi = choose_best_feather_split(a_data_set)
        best_property_name = a_property_names[bi]
        dt = split_data_set_to_dict(a_data_set, bi)
        # pv: Property Value, vt: splitted_data_set
        for (pv, vt) in dt.items():
            # 计算vt中的分类有多少个
            ls = set([t[-1] for t in vt])
            if len(ls) == 1:
                # vt中的分类个数为1, 说明这个分支分类完成
                dt[pv] = tuple(ls)[0]
            elif len(a_property_names) == 1:
                dt_value = {}
                total = 0
                label_combo = ""
                for t in vt:
                    dt_value[t[-1]] = dt_value.get(t[-1], 0) + 1
                    total += 1
                for (k, v) in dt_value.items():
                    label = "%s(%f) " % (k, v/float(total))
                    label_combo += label
                dt[pv] = {a_property_names[0]: label_combo}
            else:
                dt[pv] = create_decision_tree(vt, remove_tuple_item(a_property_names, bi))
        return {best_property_name: dt}




