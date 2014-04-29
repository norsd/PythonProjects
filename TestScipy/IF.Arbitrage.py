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

client = MongoClient('mongodb://localhost:27017/')
dbTest = client.Test

strStart = "2014-04-20 9:15:00"
strEnd = "2014-04-25 15:15:00"

data0 = []
data1 = []

if dbTest.IF0.count() == 0:
    w.start(waitTime=10)
    if0 = "IF1405.CFE"
    wdatas = w.wsi(if0,"open","2014-04-20 9:15:00", "2014-04-25 15:15:00")
    data0 = wdatas.Data[0]
    docs =[ {'_id':x[0],'open':x[1]} for x in  zip(wdatas.Times, data0) ]
    dbTest.IF0.insert(docs)
else:
    data0 = [ x[u'open'] for x in dbTest.IF0.find()]

if dbTest.IF1.count() == 0:
    w.start(waitTime=10)
    if1 = "IF1406.CFE"
    wdatas = w.wsi(if1,"open","2014-04-20 9:15:00", "2014-04-25 15:15:00")
    data1 = wdatas.Data[0]
    docs =[ {'_id':x[0],'open':x[1]} for x in  zip(wdatas.Times, data1) ]
    dbTest.IF1.insert(docs)
else:
    data1 = [ x[u'open'] for x in dbTest.IF1.find()]


lna = [ math.log(x[1]/x[0]) for x in zip(data0,data0[1:]) ]


test = _draw(lna,30)
test2 = [ len(a) for a in test]
print test2


mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
# the histogram of the data
n, bins, patches = plt.hist(lna, 50, normed=1, facecolor='g', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()


#print test




x = np.array(data0)
y = np.array(data1)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)

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

