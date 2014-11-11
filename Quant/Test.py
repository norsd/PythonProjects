__author__ = 'di_shen_sh@163.com'

from DataCenter import *
from norlib.graphics import *

datacenter = DataCenter("mongodb://localhost:27017/")
klinecol = datacenter.IF当月[300]

klines = klinecol.getdatas(20130101, 20140701)
pairs = [(i,k) for i, k in enumerate(klines) if k.SolidLength>= 15]

indexs, datas=zip(*pairs)

nextklines = [klines[i+1] for i in indexs]
nextlengths = [klines[i+1].SolidLength for i in indexs]
datetimes = [klines[i+1].Time for i in indexs]

def _onbar(a_index):
    print(datetimes[a_index])
    kl = nextklines[a_index]

    print("Upper:{0}\r\nLower:{1}".format(kl.HighLength, kl.LowLength))

bar.draw(nextlengths, _onbar)
#hist.draw(nextlengths, len(nextlengths))


#print(len(datas))
#print(datas[0])
#print(klines.Count)


