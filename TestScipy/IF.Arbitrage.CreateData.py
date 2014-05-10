#coding: utf-8
__author__ = 'di_shen_sh'

#根据参数创建样本数据,存入Mongodb
#根据不同L
#计算N(d1),N(d2)

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
    if col.count() == 0:
        w.start(waitTime=10)
        wdatas = w.wsi(a_ifId,"open,close",a_begin,a_end)
        datasOpen = wdatas.Data[0]
        datasClose = wdatas.Data[1]
        docs =[ {'_id':x[0],'open':x[1],'close':x[2] } for x in  zip(wdatas.Times, datasOpen, datasClose) ]
        col.insert(docs)
    else:
        datasClose = [ x[u'close'] for x in col.find()]
    return datasClose[:a_max]

#将d1,d2数据写入数据库
#同时计算每个数据的N
def _WriteDNs(a_datas1, a_datas2 , a_L , a_tilde = False):
    collection = "L_%s" % a_L
    if a_tilde: collection = "L_%s_tilde" % a_L
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[collection]
    if a_tilde:
        docs = [ {'_id':i ,'d1':x[0] , 'N1':norm.cdf(-x[0]), 'd2':x[1] , 'N2':norm.cdf(-x[1])} for i, x in enumerate(zip( a_datas1,a_datas2))]
    else:
        docs = [ {'_id':i ,'d1':x[0] , 'N1':norm.cdf(x[0]), 'd2':x[1] , 'N2':norm.cdf(x[1])} for i, x in enumerate(zip( a_datas1,a_datas2))]
    col.insert(docs)
    return


start = "2013-10-22 9:14:00"
end = "2013-10-30 15:15:00"
if0 = "IF1311.CFE"
if1 = "IF1312.CFE"

datas0 = _GetDatas(if0,start,end,952)
datas1 = _GetDatas(if1,start,end,952)

datas00 = _GetDatas(if0,start,end,952*2)[952:]
datas11 = _GetDatas(if1,start,end,952*2)[952:]

x = np.array(datas0)
y = np.array(datas1)


def _CalcD1( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = math.log(1+( c-l )/((1-beta)*f))
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return (p1-p2)/p3
def _CalcD2( epl , l , sigmaEpl ):
    return (epl - L)/float(sigmaEpl)

def _CalcD1t_e( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = 1+( l-c )/((1-beta)*f)#difference with _CalcD2
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return math.log(p1-p2)/p3 #difference with _CalcD2
def _CalcD1t( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = math.log( 1+( l-c )/((1-beta)*f))#difference with _CalcD2
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return (p1-p2)/p3 #difference with _CalcD2
def _CalcD2t( epl , l , sigmaEpl ):
    return (epl + L)/float(sigmaEpl)#difference with _CalcD2


Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)
#Ls = (0,0.2,0.4,0.6,0.8,1.0,1.2,1.3)
C=0.4
deltaT = 5/float(245)
alpha = -14.92827
beta = 1.006659
mu = -0.009989931
sigma = 0.169528455
sigmaEpsilon = 0.488194524

for L in Ls:
    d1s = [ _CalcD1(x,C,L,beta,mu,sigma,deltaT)  for x in datas00 ]
    d2s = [ _CalcD2( x[1] - (alpha + beta*x[0]) , L , sigmaEpsilon ) for x in zip(datas00,datas11) ]
    _WriteDNs( d1s, d2s, L)

    d1s_t = [ _CalcD1t(x,C,L,beta,mu,sigma,deltaT)  for x in datas00 ]
    d2s_t = [ _CalcD2t( x[1] - (alpha + beta*x[0]) , L , sigmaEpsilon ) for x in zip(datas00,datas11) ]
    _WriteDNs( d1s_t, d2s_t, L, True)
    #print norm.cdf(d2s)

