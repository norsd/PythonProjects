#coding: utf-8
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
from itertools import izip

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
def _GetDNs( a_L , a_tilde = False ):
    collection = "L_%s" % (a_L)
    if a_tilde:collection = "L_%s_tilde" % a_L
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[collection]
    n1 = [ x[u'N1'] for x in col.find()]
    n2 = [ x[u'N2'] for x in col.find()]
    return n1,n2
def _GetL( a_index):
    return 0
class Account:
    def __init__(self, a_cash):
        self.__cash = a_cash
        self.__dtVariety = {}
        self.__dtLPos = {}
        self.__dtSPos = {}
        self.__dtOrder = {}
        self.__margin = 0.0
    def AddContractInfo(self, a_name, a_multiplier, a_margin):
        self.__dtVariety[a_name] = (a_name, a_multiplier, a_margin)
        return
    def Open(self, a_name, a_price, a_count ):
        if a_count == 0:
            return False #不合逻辑的开仓
        if not self.__dtVariety.has_key(a_name):
            return False #没有这个Variety信息
        vi = self.__dtVariety[a_name]
        c = abs(a_count)
        require = c*a_price*vi[1]*vi[2]
        if self.__cash < require:
            return False #可用资金不足
        self.__cash -= require
        if a_count > 0:
            pos = self.__dtLPos.get(a_name, [0,0])
            pos[0] = (pos[0]*pos[1] + a_price*c) / float(pos[1] + c) #仓位均价
            pos[1] = pos[1] + c #仓位数
            self.__dtLPos[a_name] = pos
        else:
            pos = self.__dtSPos.get(a_name, [0,0])
            pos[0] = (pos[0]*pos[1] + a_price*c) / float(pos[1] + c) #仓位均价
            pos[1] = pos[1] + c #仓位数
            self.__dtSPos[a_name] = pos
        return
    def Close(self, a_name, a_price, a_count):
        if a_count == 0:
            return False #不合逻辑的平仓
        if not self.__dtVariety.has_key(a_name):
            return False #没有这个Variety信息
        vi = self.__dtVariety[a_name]
        if a_count > 0:
            c = a_count
            if not self.__dtLPos.has_key(a_name):
                return False #没有持仓信息
            pos = self.__dtLPos[a_name]
            pos[1] = pos[1] - c #仓位数
            self.__cash += pos[0]*c*vi[1]*vi[2] + (a_price-pos[0])*c*vi[1]
        else:
            c = -a_count
            pos = self.__dtSPos.get(a_name, [0,0])
            pos[1] = pos[1] - c #仓位数
            self.__cash += pos[0]*c*vi[1]*vi[2] + (pos[0]-a_price)*c*vi[1]
        return

start = "2013-10-22 9:14:00"
end = "2013-10-30 15:15:00"
if0 = "IF1311.CFE"
if1 = "IF1312.CFE"

datas00 = _GetDatas(if0,start,end,952*2)[952:]
datas11 = _GetDatas(if1,start,end,952*2)[952:]

long = 0
short = 0
openTrd = 0.7
closeTrd = 0.4
acc = Account(300000)
acc.AddContractInfo(if0,300,0.15)
acc.AddContractInfo(if1,300,0.15)

for i,ifps in enumerate(izip(datas00,datas11)):
    p0 = ifps[0]
    p1 = ifps[1]
    bullL = _GetL(True)
    bearL = _GetL(False)
    if bullL > openTrd:
        acc.Open(if0, p0,  1)
        acc.Open(if1, p1, -1)
    if bullL > closeTrd:
        acc.Close(if0, p0,  1)
        acc.Close(if1, p1, -1)
    if bearL > openTrd:
        acc.Open(if0, p0, -1)
        acc.Open(if1, p1,  1)
    if bearL > closeTrd:
        acc.Close(if0, p0, -1)
        acc.Close(if1, p1,  1)



Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)

