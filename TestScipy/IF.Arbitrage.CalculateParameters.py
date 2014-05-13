# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

import pymongo as mo
from pymongo import MongoClient
import math

from scipy import stats
from scipy.stats import norm
import numpy as np
import pylab
import matplotlib.pyplot as plt


from WindPy import w
from datetime import *

#获取数据
#a_ifname形如"IF1401.CFE"
#a_begin开始时间
#a_end结束时间
#a_max表示最多读取a_max个数据
def _GetDatas(a_ifId, a_begin, a_end , a_max ):
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[a_ifId]
    colRange = client.Test["range_%s" % a_ifId]
    if not col.count == 0:
        #检测是否给定的时间范围
        #否则重置col,colRange
        if colRange.count() == 0:
            col.drop()
        else:
            range = [ x[u'_id'] for x in colRange.find()]
            if not (range[0] == a_ifId and range[1] == a_begin and range[2] == a_end):
                colRange.drop()
                col.drop()
    if col.count() == 0:
        w.start(waitTime=10)
        wdatas = w.wsi(a_ifId,"open,close",a_begin,a_end)
        datasOpen = wdatas.Data[0]
        datasClose = wdatas.Data[1]
        docs =[ {'_id':x[0],'open':x[1],'close':x[2] } for x in  zip(wdatas.Times, datasOpen, datasClose) ]
        col.insert(docs)
        colRange.insert(  [ {'_id':a_ifId} , {'_id':a_begin} , {'_id':a_end}] )
    else:
        datasClose = [ x[u'close'] for x in col.find()]
    return datasClose[:a_max]

start = "2013-10-22 9:14:00"
end = "2013-10-30 15:15:00"
if0 = "IF1311.CFE"
if1 = "IF1312.CFE"

#start = "2014-05-03 9:14:00"
#end = "2014-05-12 15:15:00"
#if0 = "IF1405.CFE"
#if1 = "IF1406.CFE"

datas0 = _GetDatas(if0,start,end,952)
datas1 = _GetDatas(if1,start,end,952)

datas00 = _GetDatas(if0,start,end,952*2)[952:]
datas11 = _GetDatas(if1,start,end,952*2)[952:]


#对数收益率
lna = [ math.log(x[1]/x[0]) for x in zip(datas0,datas0[1:]) ]
mu_if0 = sum(lna)/len(lna)
ex = mu_if0
sigma_if0 = (sum( [ (ex-x)**2 for x in lna ] )/(len(lna)-1))**0.5
#print "numpy mu:%s sigma:%s" % (np.mean(h) , np.std(h)) np.std标准差,不是样本标准差
#Correct mu,sigma
muC = mu_if0*270
sigmaC =  (sigma_if0**2*270*245)**0.5
#print "day_mu: %s  year_sigma:  %s" %( muC , sigmaC)

x = np.array(datas0)
y = np.array(datas1)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
print "%s = %s + %s * %s" %(if1, intercept, slope , if0)
#sigmaEpsilon
a = intercept
b = slope
deltasEpsilon = [ x[1] - a - b*x[0]  for x in zip(datas0,datas1)]
ds = deltasEpsilon[:]
sigmaEpsilon =  stats.tstd(ds)   #Calculate "Sample Variance"! do not use np.std(ds) or np.var(ds)

client = MongoClient('mongodb://localhost:27017/')
colParameter = client.Test["Parameter"]
colParameter.save({'_id':'now','start':start,'end':end,'if0':if0,'if1':if1, 'a':a, 'b':b ,'sigmaEpsilon':sigmaEpsilon,'mu':muC,'sigma':sigmaC})

# Calculate some additional outputs
# Plotting
x = np.array(datas0)
y = np.array(datas1)
predict_y = intercept + slope * x
pylab.plot(x, y, 'o')
pylab.plot(x, predict_y, 'k-')
pylab.show()

h = lna[:]
h.sort()
fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
plt.plot(h,fit,'-o')
n, bins, patches = plt.hist(lna, 50, normed=1, facecolor='g', alpha=0.75)
plt.grid(True)
plt.show()


#alpha = -14.92827
#beta = 1.006659
#sigmaEpsilon = 0.488194524
#mu = -0.009989931
#sigma = 0.169528455
print "alpha = %s" % a
print "beta = %s" % b
print "sigmaEpsilon = %s" % sigmaEpsilon
print "mu = %s" % muC
print "sigma = %s" % sigmaC
