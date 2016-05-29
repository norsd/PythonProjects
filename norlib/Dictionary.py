# coding:utf-8
from typing import Dict

__author__ = 'di_shen_sh@163.com'


def get_value(a_dict: Dict, a_key: object, a_default_value: object):
    a_dict.setdefault(a_key, a_default_value)
    return a_dict[a_key]