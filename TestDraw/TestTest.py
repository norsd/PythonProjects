__author__ = 'Administrator'
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
#import dateutil as tz
from dateutil import tz
from math import e

def UtcToLocal( arg_dtime ):
    from_zone = tz.gettz('UTC')
    #to_zone = tz.gettz('CST')
    to_zone = tz.tzlocal()
    # Tell the datetime object that it's in UTC time zone
    utc = arg_dtime.replace(tzinfo=from_zone)
    # Convert time zone
    return utc.astimezone(to_zone)

def Filter( arg_myranges , arg_dFilter ):
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

datas = []
deltas = []
absdeltas = []
times =[]
d=0
i=0
for data in datasQ:
    datas.append(data)
    d= (data["priceE"]-data["priceB"])
    absd = np.abs(d)
    absdeltas.append(absd)
    deltas.append(d)
    if d<1:
        i=i+1
    times.append( UtcToLocal(data["_id"]))
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


