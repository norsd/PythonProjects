#coding: utf-8
__author__ = 'di_shen_sh'

from itertools import izip
from scipy import stats
import math
import numpy as np

#计算两个序列的相关性 datas1 = a + b*datas0
#根据datas0的对数收益率计算 dFt = uFt + sigmaFt*dZt
#返回 a,b,sigmaEpsilon,mu,sigma,lna
def CreateParameters(a_datas0, a_datas1):
    #对数收益率
    lna = [math.log(x[1]/x[0]) for x in zip(a_datas0, a_datas0[1:])]
    mu_if0 = sum(lna)/len(lna)
    ex = mu_if0
    sigma_if0 = (sum( [ (ex-x)**2 for x in lna ] )/(len(lna)-1))**0.5
    #print "numpy mu:%s sigma:%s" % (np.mean(h) , np.std(h)) np.std标准差,不是样本标准差
    #Correct mu,sigma
    muC = mu_if0*270
    sigmaC = (sigma_if0**2*270*245)**0.5

    x = np.array(a_datas0)
    y = np.array(a_datas1)
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)

    a = intercept
    b = slope
    deltasEpsilon = [x[1] - a - b*x[0] for x in izip(a_datas0, a_datas1)]
    sigmaEpsilon = stats.tstd(deltasEpsilon)   #Calculate "Sample Variance"! do not use np.std(ds) or np.var(ds)

    return intercept,slope,sigmaEpsilon,muC,sigmaC,lna  #返回 a,b,sigmaEpsilon,mu,sigma,lna