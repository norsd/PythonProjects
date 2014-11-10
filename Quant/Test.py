__author__ = 'di_shen_sh@163.com'

from DataCenter import *

datacenter = DataCenter("mongodb://localhost:27017/")
klines = datacenter.IF当月[300]

pairs = [(i,k) for i, k in enumerate(klines.getdatas(20140101, 20141101)) if k.SolidLength>= 12]

indexs, datas= zip(*pairs)

nextis = [i+1 for i in indexs]

print(indexs)
print(nextis)

print(datas)
#print(len(datas))
#print(datas[0])
#print(klines.Count)


