# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

from pymongo import MongoClient
from scipy import stats

import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import Tools


#start = "2013-10-22 9:14:00"
#end = "2013-10-30 15:15:00"
#if0 = "IF1311.CFE"
#if1 = "IF1312.CFE"

start = "2014-05-03 9:14:00"
end = "2014-05-12 15:15:00"
if0 = "IF1405.CFE"
if1 = "IF1406.CFE"

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

Tools.WriteCurrentParameters(start, end, if0, 300, 0.15, if1, 300, 0.15, a, b, sigmaEpsilon, muC, sigmaC)

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
