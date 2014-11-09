__author__ = 'di_shen_sh@163.com'

from DataCenter import *

datacenter = DataCenter("mongodb://localhost:27017/")
klines = datacenter.IF当月[300]



