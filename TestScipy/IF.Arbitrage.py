# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

import pymongo as mo
from pymongo import MongoClient

import math

from scipy import stats
import numpy as np
import pylab
import matplotlib.pyplot as plt

from WindPy import w
from datetime import *

def _GetDatas(a_ifname, a_start, a_end , a_max ):
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[a_ifname]
    if col.count() == 0:
        w.start(waitTime=10)
        wdatas = w.wsi(a_ifname,"open,close",a_start,a_end)
        datasOpen = wdatas.Data[0]
        datasClose = wdatas.Data[1]
        docs =[ {'_id':x[0],'open':x[1],'close':x[2] } for x in  zip(wdatas.Times, datasOpen, datasClose) ]
        col.insert(docs)
    else:
        datasClose = [ x[u'close'] for x in col.find()]
    return datasClose[:a_max]


strStart = "2014-04-20 9:15:00"
strEnd = "2014-04-25 15:15:00"

start = "2013-10-22 9:14:00"
end = "2013-10-30 15:15:00"
if0 = "IF1311.CFE"
if1 = "IF1312.CFE"

datas0 = _GetDatas(if0,start,end,952)
datas1 = _GetDatas(if1,start,end,952)



x = np.array(datas0)
y = np.array(datas1)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)

print "%s = %s + %s * %s" %(if1, intercept, slope , if0)


lna = [ math.log(x[1]/x[0]) for x in zip(datas0,datas0[1:]) ]
#lna = [ abs(x[1]-x[0]) for x in zip(data0,data0[1:])]
#lna.sort()


mu_if0 = sum(lna)/len(lna)
ex = mu_if0
sigma_if0 = (sum( [ (ex-x)**2 for x in lna ] )/len(lna))**0.5
print mu_if0,sigma_if0

h = lna
h.sort()
print "np %s %s" % (np.mean(h) , np.std(h))

#Correct mu,sigma
muC = mu_if0*270
sigmaC =  (sigma_if0**2*270*245)**0.5

print "%s , %s" %( muC , sigmaC)

#sigmaEpsilon
a = intercept
b = slope
deltasEpsilon = [ x[1] - a - b*x[0]  for x in zip(datas0,datas1)]
ds = deltasEpsilon[:].sort()
sigmaEpsilon = np.std(ds)



fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
plt.plot(h,fit,'-o')



# the histogram of the data
n, bins, patches = plt.hist(lna, 50, normed=1, facecolor='g', alpha=0.75)
#plt.xlabel('Smarts')
#plt.ylabel('Probability')
#plt.title('Histogram of IQ')
plt.grid(True)
plt.show()




# Calculate some additional outputs
predict_y = intercept + slope * x
pred_error = y - predict_y
degrees_of_freedom = len(x) - 2
residual_std_error = np.sqrt(np.sum(pred_error**2) / degrees_of_freedom)

# Plotting
pylab.plot(x, y, 'o')
pylab.plot(x, predict_y, 'k-')
pylab.show()

print  'y = %s + %s * x' % (intercept, slope)



#将datas中的数据升序排列后分成count个子数组返回
def _draw( datas , count ):
    ret = [ [] for x in range(0, count) ]
    datas.sort()
    min = datas[0]
    max = datas[-1]
    delta = (max-min)/count
    di = 0
    for i in range(0,count):
        for j in range(di, len(datas)):
            if( datas[j]<= min + (i+1)*delta ):
                ret[i].append(datas[j])
            else:
                di = j
                break
    return ret
