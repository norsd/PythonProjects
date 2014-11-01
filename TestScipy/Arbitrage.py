#coding: utf-8
__author__ = 'di_shen_sh'

from itertools import izip
from scipy import stats
import math
import numpy as np
import Tools

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

#返回
#return:
#0:len(datas00)个 bull在Ls中N(d1)*N(d2)的最大值
#1:len(datas00)个 bear在Ls中N(d1)*N(d2)的最大值
def CalculateD1D2(a_Ls, a_C, a_a, a_b, a_sigmaEpsilon, a_mu, a_sigma, a_deltaT, a_datas00, a_datas11):
    C = a_C
    alpha = a_a
    beta = a_b
    sigmaEpsilon = a_sigmaEpsilon
    mu = a_mu
    sigma = a_sigma
    deltaT = a_deltaT
    datas00 = a_datas00
    datas11 = a_datas11
    retBullMax = []
    retBearMax = []

    print "alpha:%s" % alpha
    ret0 = []
    #纵截面
    for L in a_Ls:
        d1s = [Tools.CalcD1_Bull(x, C, L, beta, mu, sigma, deltaT) for x in datas00]
        d2s = [Tools.CalcD2_Bull(x[1] - (alpha + beta*x[0]), L, sigmaEpsilon) for x in izip(datas00, datas11)]
        #Tools.WriteDNs(d1s, d2s, L)
        d1s_bear = [Tools.CalcD1_Bear(x, C, L, beta, mu, sigma, deltaT) for x in datas00]
        d2s_bear = [Tools.CalcD2_Bear(x[1] - (alpha + beta*x[0]), L, sigmaEpsilon) for x in izip(datas00, datas11)]
        #Tools.WriteDNs( d1s_bear, d2s_bear, L, True)
        Nx_bull = [ stats.norm.cdf(d1)*stats.norm.cdf(d2) for d1,d2 in izip(d1s,d2s)]
        Nx_bear = [ stats.norm.cdf(-d1)*stats.norm.cdf(-d2) for d1,d2 in izip(d1s_bear,d2s_bear)]

        ret0.append((Nx_bull, Nx_bear))
    #横截面
    lCount = len(a_Ls)
    for i in range(0, len(datas00)):
        bulls = []
        bears = []
        for j in range(0, lCount):
            bulls.append(ret0[j][0][i])
            bears.append(ret0[j][1][i])
        retBullMax.append(max(bulls))
        retBearMax.append(max(bears))

    print retBullMax
    print retBearMax
    return retBullMax, retBearMax