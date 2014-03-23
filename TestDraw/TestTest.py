__author__ = 'Administrator'
from pymongo import MongoClient
import math
import matplotlib.pyplot as plt
import numpy as np
#import dateutil as tz
from dateutil import tz
from math import e


def UtcToLocal(arg_dtime):
    from_zone = tz.gettz('UTC')
    #to_zone = tz.gettz('CST')
    to_zone = tz.tzlocal()
    # Tell the datetime object that it's in UTC time zone
    utc = arg_dtime.replace(tzinfo=from_zone)
    # Convert time zone
    return utc.astimezone(to_zone)


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
print datasQ.count()


for data in datasQ:
    print data.priceE

datas = []
deltas = []
absdeltas = []
times = []
d=0
i=0
for data in datasQ:
    datas.append(data)
    d = (data["priceE"]-data["priceB"])
    absd = np.abs(d)
    absdeltas.append(absd)
    deltas.append(d)
    if d < 1:
        i += 1
    times.append(UtcToLocal(data["_id"]))
print i


#a = plt.hist( deltas,bins=40,histtype='stepfilled' )

#plt.figure(1)
#plt.subplot(611).hist( deltas,bins=40,histtype='stepfilled' )

p1 = plt.subplot(612)
p1.plot(times,deltas)

print (times)
print (deltas)
#deltasFilter = Filter(datas,1.2)
#plt.subplot(613).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,1)
#plt.subplot(614).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0.8)
#plt.subplot(615).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0.6)
#plt.subplot(616).hist(deltasFilter,bins=40)
#deltasFilter = Filter(datas,0)
#plt.subplot(616).hist(deltasFilter,bins=40)

plt.show()


class _Range:
    def __init__(self, priceS, priceE, timeS, timeE):
        self.priceS= priceS
        self.priceE = priceE
        self.timeS = timeS
        self.timeE = timeE
    def GetDelta(self):
        return self.priceE-self.priceS
    def GetTrend(self):
        if self.priceS < self.priceE:
            return 1
        if self.priceS == self.priceE:
            return 0
        return 1


class Range:
    def __init__(self, range0, threshold):
        self.s = range0.priceS
        self.e = range0.priceE
        self.c = range0.priceE
        self.st = range0.timeS
        self.et = range0.timeE
        self.ct = range0.timeE
        self.t = threshold
    def GetTrend(self):
        d0 = self.e - self.s
        d1 = self.c - self.s
        if d0 * d1 <= 0:
            raise "range logical error"
        if d0 > 0:
            return 1
        if d0 == 0:
            return 0
        if d0 < 0:
            return -1
    def GetDelta(self):
        return self.e-self.s
    def GetAbsDelta(self):
        return math.fabs(self.GetDelta())
    def Add(self, range1):
        if range1.GetTrend() == self.GetTrend():
            self.e = range1.priceE
            self.c = range1.priceE
            self.et = range1.timeE
            self.ct = range1.timeE
            return True
        elif range1.GetAbsDelta() > self.t:
            return False
        else:
            self.e = range1.priceE
            self.c = range1.pr


