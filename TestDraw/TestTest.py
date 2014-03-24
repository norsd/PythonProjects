__author__ = 'Administrator'
from pymongo import MongoClient
import math
import matplotlib.pyplot as plt
import numpy as np
#import dateutil as tz

from math import e
from norlib_python import *
from norlib_python.DateTime import *


class _Range:
    def __init__(self, priceB, priceE, timeB, timeE):
        self.priceB= priceB
        self.priceE = priceE
        self.timeB = timeB
        self.timeE = timeE
    def GetDelta(self):
        return self.priceE-self.priceB
    def GetTrend(self):
        if self.priceB < self.priceE:
            return 1
        if self.priceB == self.priceE:
            return 0
        return 1
    def GetAbsDelta(self):
        return abs(self.GetDelta())


class Range:
    def __init__(self, range0, threshold):
        self.b = range0.priceB
        self.e = range0.priceE
        self.c = range0.priceE
        self.bt = range0.timeB
        self.et = range0.timeE
        self.ct = range0.timeE
        self.t = threshold
    def GetTrend(self):
        d0 = self.e - self.b
        d1 = self.c - self.b
        if d0 * d1 <= 0:
            raise "range logical error"
        if d0 > 0:
            return 1
        if d0 == 0:
            return 0
        if d0 < 0:
            return -1
    def GetDelta(self):
        return self.e-self.b
    def GetAbsDelta(self):
        return abs(self.GetDelta())
    def Add(self, range1):
        if range1.GetAbsDelta() > self.t and range1.GetTrend()!=self.GetTrend():
            return False
        self.e = range1.priceE
        self.et = range1.timeE
        if range1.GetTrend() == self.GetTrend() and range1.GetAbsDelta()>self.GetAbsDelta():
            self.c = range1.priceE
            self.ct = range1.timeE
        return True


def Filter(arg_myranges, arg_dFilter):
    datas = arg_myranges
    deltasFilter= []
    f=arg_dFilter
    n= len(datas)
    for i in range(1,n):
        dataPre = datas[i-1]
        dataCur = datas[i]
        d1 = (dataPre["priceE"]-dataPre["priceB"])
        d0 =(dataCur["priceE"]-dataCur["priceB"])
        if d1*d0>0:
            deltasFilter[-1]+=d0
        elif np.abs(d0)>f:
            deltasFilter.append(d0)
        else:
            deltasFilter[-1] += d0
    return np.abs(deltasFilter)

m = MongoClient('localhost')
m.test.authenticate('sa', 'norsd@163.com')

datasQ = m.test.MyRanges.find()



deltas = []
absdeltas = []
times = []

datas = []
dataranges = []
datarangeExs = []
deltaExs = []

for data in datasQ:
    datas.append(data)
    d = (data["priceE"]-data["priceB"])
    absd = np.abs(d)
    absdeltas.append(absd)
    deltas.append(d)
    times.append(UtcToLocal(data["_id"]))
    #_Range
    r = _Range(data["priceB"],data["priceE"],data["_id"],data["timeE"])
    dataranges.append(r)

print absdeltas
datarangeExs.append( Range(dataranges[0],0.6))
for i in range(1,len(dataranges)):
    if not datarangeExs[-1].Add(r):
        deltaExs.append(datarangeExs[-1].GetAbsDelta())
        datarangeExs.append( Range(r,0.6) )

print deltaExs




#a = plt.hist( deltas,bins=40,histtype='stepfilled' )
#plt.figure(1)
plt.subplot(611).hist( deltas,bins=40,histtype='stepfilled' )
p1 = plt.subplot(612)
p1.plot(times,deltas)
#deltasFilter = Filter(datas,1.2)
plt.subplot(613).hist(deltaExs,bins=40)
#deltasFilter = Filter(datas,1)
#plt.subplot(614).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0.8)
#plt.subplot(615).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0.6)
#plt.subplot(616).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0)
#plt.subplot(616).hist(deltasFilter,bins=40)
plt.show()






