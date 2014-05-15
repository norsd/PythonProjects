# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

from pymongo import MongoClient
from scipy import stats

import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import Tools

key1 = "IF"
key2 = 2

if key1 == "IF":
    if key2 == 0:
        start = "2013-10-22 9:14:00"
        end = "2013-10-30 15:15:00"
        if0 = "IF1311.CFE"
        if1 = "IF1312.CFE"
    elif key2 ==1:
        start = "2014-05-03 9:00:00"
        end = "2014-05-12 15:00:00"
        if0 = "IF1406.CFE"
        if1 = "IF1405.CFE"
    elif key2 == 2:
        start = "2014-05-12 9:00:00"
        end = "2014-05-15 15:15:00"
        if0 = "IF1406.CFE"
        if1 = "IF1405.CFE"
    multiplier0 = 300
    margin0 = 0.15
    multiplier1 = 300
    margin1 = 0.15
elif key1 == "RU":
    if key2 == 0:
        start = "2014-05-03 9:00:00"
        end = "2014-05-12 15:00:00"
    elif key2 ==1:
        start = "2014-04-03 9:00:00"
        end = "2014-04-12 15:00:00"
    if0 = "RU1409.SHF"
    if1 = "RU1501.SHF"
    multiplier0 = 10
    margin0 = 0.15
    multiplier1 = 10
    margin1 = 0.15

nSampleCount = 952
datas0 = Tools.GetDatas(if0,start,end,952)
datas1 = Tools.GetDatas(if1,start,end,952)

datas00 = Tools.GetDatas(if0,start,end,952*2)[952:]
datas11 = Tools.GetDatas(if1,start,end,952*2)[952:]


#对数收益率
lna = [ math.log(x[1]/x[0]) for x in zip(datas0,datas0[1:]) ]
mu_if0 = sum(lna)/len(lna)
ex = mu_if0
sigma_if0 = (sum( [ (ex-x)**2 for x in lna ] )/(len(lna)-1))**0.5
#print "numpy mu:%s sigma:%s" % (np.mean(h) , np.std(h)) np.std标准差,不是样本标准差
#Correct mu,sigma
muC = mu_if0*270
sigmaC = (sigma_if0**2*270*245)**0.5
#print "day_mu: %s  year_sigma:  %s" %( muC , sigmaC)

x = np.array(datas0)
y = np.array(datas1)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
print "%s = %s + %s * %s" %(if1, intercept, slope , if0)
a = intercept
b = slope
deltasEpsilon = [ x[1] - a - b*x[0]  for x in zip(datas0,datas1)]
ds = deltasEpsilon[:]
sigmaEpsilon = stats.tstd(ds)   #Calculate "Sample Variance"! do not use np.std(ds) or np.var(ds)

Tools.WriteCurrentParameters(start, end, if0, multiplier0, margin0, if1, multiplier1, margin1, a, b, sigmaEpsilon, muC, sigmaC)

# Calculate some additional outputs
# Plotting
x = np.array(datas0)
y = np.array(datas1)
predict_y = intercept + slope * x

fig = pylab.figure()
plot0 = fig.add_subplot(311)
plot1 = fig.add_subplot(312)
plot2 = fig.add_subplot(313)

#pylab.plot(x, y, 'o')
#pylab.plot(x, predict_y, 'k-')
#pylab.show()
plot0.plot(x,y,'o')
plot0.plot(x, predict_y, 'k-')

plt.ylabel('%s - %s'%(if1,if0))
plot1.plot(range(0, len(x)), y-x, '-')


h = lna[:]
h.sort()
fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
plot2.plot(h, fit, '-o')

n, bins, patches = plot2.hist(lna, 50, normed=1, facecolor='g', alpha=0.75)

plot2.grid(True)

fig.suptitle('%s  -   %s \n %s  -  %s \n %s = %s + %s * %s '%(if0, if1, start, end, if1, a, b, if0), fontsize=14, fontweight='bold')

pylab.show() #fig.show()会一闪而过






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
