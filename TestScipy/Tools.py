# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'


from pymongo import MongoClient
from scipy import stats
from itertools import izip
from WindPy import w
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab

#获取数据
#a_ifname形如"IF1401.CFE"
#a_begin开始时间
#a_end结束时间
#a_max表示最多读取a_max个数据,-1表示读取所有数据
def GetDatas(a_ifId, a_begin, a_end, a_max):
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
        wdatas = w.wsi(a_ifId,"open,close",a_begin,a_end, 'Fill=Previous')
        datasOpen = wdatas.Data[0]
        datasClose = wdatas.Data[1]
        docs =[ {'_id':x[0],'open':x[1],'close':x[2] } for x in  zip(wdatas.Times, datasOpen, datasClose) ]
        col.insert(docs)
        colRange.insert(  [ {'_id':a_ifId} , {'_id':a_begin} , {'_id':a_end}] )
    else:
        datasClose = [ x[u'close'] for x in col.find()]
    if a_max == -1:
        return datasClose
    return datasClose[:a_max]


_dtDatas = {}
#仅从内存或者数据库获取数据
def GetDatas2(a_ifId, a_index, a_count):
    if not _dtDatas.has_key(a_ifId):
        client = MongoClient('mongodb://localhost:27017/')
        col = client.Test[a_ifId]
        datasClose = [ x[u'close'] for x in col.find()]
        _dtDatas[a_ifId] = datasClose
    return _dtDatas[a_ifId][a_index:(a_index + a_count)]

#清空_dtDatas
def ResetDatas2():
    _dtDatas.clear()

#a_datas0:数据序列0
#a_datas1:数据序列1
#a_a: alpha
#a_b: beta
#a_ln0s: 数据序列0的对数收益率
def Show0(a_name0, a_name1, a_start, a_datas0, a_datas1, a_a, a_b, a_ln0s):
    fig = pylab.figure()
    plot0 = fig.add_subplot(311)
    plot1 = fig.add_subplot(312)
    plot2 = fig.add_subplot(313)
    plot0.plot(a_datas0, a_datas1, 'o')
    plot0.plot(a_datas0, [a_a + x*a_b for x in a_datas0], 'k-')
    plot1.plot([d1-d0 for d0, d1 in izip(a_datas0,a_datas1)], '-')
    #plt.ylabel('%s - %s'%(if1,if0))
    #plot1.plot(range(0, len(x)), y-x, '-')
    h = a_ln0s[:]
    h.sort()
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
    plot2.plot(h, fit, '-o')
    n, bins, patches = plot2.hist(a_ln0s, 50, normed=1, facecolor='g', alpha=0.75)
    plot2.grid(True)
    fig.suptitle('%s  -   %s \n %s - ? \n %s = %s + %s * %s ' % (a_name0, a_name1, a_start, a_name1, a_a, a_b, a_name0), fontsize=14, fontweight='bold')
    pylab.show() #fig.show()会一闪而过


#将d1,d2数据写入数据库
#同时计算每个数据的N
def WriteDNs(a_datas1, a_datas2 , a_L , a_bear = False):
    collection = "L_%s_%s" % (a_L ,  (a_bear and ['bear'] or ['bull'])[0] )
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[collection]
    col.drop()
    if a_bear:
        docs = [ {'_id':i ,
                  'd1':x[0] , 'N1':norm.cdf(-x[0]),
                  'd2':x[1] , 'N2':norm.cdf(-x[1])} for i, x in enumerate(izip( a_datas1,a_datas2))]
    else:
        docs = [ {'_id':i ,
                  'd1':x[0] , 'N1':norm.cdf(x[0]),
                  'd2':x[1] , 'N2':norm.cdf(x[1])} for i, x in enumerate(izip( a_datas1,a_datas2))]
    col.insert(docs)
    return

def GetDNs( a_L , a_bear = False ):
    collection = "L_%s_%s" % (a_L ,  (a_bear and ['bear'] or ['bull'])[0] )
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[collection]
    n1 = [ x[u'N1'] for x in col.find()]
    n2 = [ x[u'N2'] for x in col.find()]
    return n1,n2



def CalcD1_Bull( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = math.log(1+( c-l )/((1-beta)*f))
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return (p1-p2)/p3
def CalcD2_Bull( epl , l , sigmaEpl ):
    return (epl - l )/float(sigmaEpl)
#方龙可能错误的熊市D1计算函数
def _CalcD1t_e( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = 1+( l-c )/((1-beta)*f)#difference with CalcD1_Bull
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return math.log(p1-p2)/p3 #difference with CalcD2_Bull
def CalcD1_Bear( f , c , l , beta , miu , sigma , t ):
    ss = sigma**2
    p1 = math.log( 1+( l-c )/((1-beta)*f))#difference with _CalcD2
    p2 = (miu - ss/2)*t
    p3 = sigma*(t**0.5)
    return (p1-p2)/p3
def CalcD2_Bear( epl , l , sigmaEpl ):
    return (epl + l)/float(sigmaEpl)#difference with CalcD2_Bull


def GetPrs(a_Ls):
    client = MongoClient('mongodb://localhost:27017/')
    datassBear = []
    datassBull = []
    prsBear = []
    prsBull = []
    for l in a_Ls:
        n1s, n2s = GetDNs(l, False)
        datassBull.append([n1*n2 for n1, n2 in izip(n1s, n2s)])
    for j in range(0, len(datassBull[0])):
        row = [datassBull[i][j] for i in range(0, len(a_Ls))]
        ok = max(row)
        prsBull.append(ok)
    for l in a_Ls:
        n1s, n2s = GetDNs(l, True)
        datassBear.append([n1*n2 for n1, n2 in izip(n1s, n2s)])
    for j in range(0, len(datassBear[0])):
        row = [datassBear[i][j] for i in range(0, len(a_Ls))]
        ok = max(row)
        prsBear.append(ok)
    return prsBull, prsBear

def GetCurrentParameters():
    client = MongoClient('mongodb://localhost:27017/')
    colParameter = client.Test["Parameter"]
    paras = colParameter.find_one({'_id': u'now'})
    start = paras[u'start']
    end = paras[u'end']
    if0 = paras[u'if0']
    if1 = paras[u'if1']
    alpha = paras[u'a']
    beta = paras[u'b']
    sigmaEpsilon = paras[u'sigmaEpsilon']
    mu = paras[u'mu']
    sigma = paras[u'sigma']
    return paras

def WriteCurrentParameters( a_start, a_end,
                            a_if0, a_multiplier0, a_margin0,
                            a_if1, a_multiplier1, a_margin1,
                            a_a, a_b, a_sigmaEpsilon, a_mu, a_sigma):
    client = MongoClient('mongodb://localhost:27017/')
    colParameter = client.Test["Parameter"]
    colParameter.save({'_id': 'now', 'start': a_start, 'end' : a_end,
                       'if0': a_if0, 'multiplier0': a_multiplier0, 'margin0': a_margin0,
                       'if1': a_if1, 'multiplier1': a_multiplier1, 'margin1': a_margin1,
                       'a': a_a, 'b': a_b, 'sigmaEpsilon': a_sigmaEpsilon, 'mu': a_mu, 'sigma': a_sigma})
