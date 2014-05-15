#coding: utf-8
__author__ = 'di_shen_sh'

#根据参数创建样本数据,存入Mongodb
#根据不同L
#计算N(d1),N(d2)

from itertools import izip

import math
import numpy as np
import Tools



paras = Tools.GetCurrentParameters()
#start = "2013-10-22 9:14:00"
#end = "2013-10-30 15:15:00"
#if0 = "IF1311.CFE"
#if1 = "IF1312.CFE"
#alpha = 12.4828837144
#beta = 0.988709825626
#sigmaEpsilon = 0.664078755299
#mu = 0.00176416816363
#sigma = 0.155309122851
start = paras[u'start']
end = paras[u'end']
if0 = paras[u'if0']
if1 = paras[u'if1']
alpha = paras[u'a']
beta = paras[u'b']
sigmaEpsilon = paras[u'sigmaEpsilon']
mu = paras[u'mu']
sigma = paras[u'sigma']


Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)
#Ls = (0,0.2,0.4,0.6,0.8,1.0,1.2,1.3)
C=0.4
deltaT = 5/float(245)


datas00 = Tools.GetDatas(if0,start,end,952*2)[952:]
datas11 = Tools.GetDatas(if1,start,end,952*2)[952:]


for L in Ls:
    d1s = [ Tools.CalcD1_Bull(x,C,L,beta,mu,sigma,deltaT)  for x in datas00 ]
    d2s = [ Tools.CalcD2_Bull( x[1] - (alpha + beta*x[0]) , L , sigmaEpsilon ) for x in izip(datas00,datas11) ]
    Tools.WriteDNs( d1s, d2s, L)

    d1s_bear = [ Tools.CalcD1_Bear(x,C,L,beta,mu,sigma,deltaT)  for x in datas00 ]
    d2s_bear = [ Tools.CalcD2_Bear( x[1] - (alpha + beta*x[0]) , L , sigmaEpsilon ) for x in izip(datas00,datas11) ]
    Tools.WriteDNs( d1s_bear, d2s_bear, L, True)
    #print norm.cdf(d2s)

