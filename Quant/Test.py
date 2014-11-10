__author__ = 'di_shen_sh@163.com'

from DataCenter import *
from norlib.graphics import *

datacenter = DataCenter("mongodb://localhost:27017/")
klinecol = datacenter.IF当月[300]

klines = klinecol.getdatas(20140101, 20141101)
pairs = [(i,k) for i, k in enumerate(klines) if k.SolidLength>= 10]

indexs, datas=zip(*pairs)


nextlengths = [klines[i+1].SolidLength for i in indexs]

bar.draw(nextlengths)


#print(len(datas))
#print(datas[0])
#print(klines.Count)


