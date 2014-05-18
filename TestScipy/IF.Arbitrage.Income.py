#coding: utf-8
__author__ = 'di_shen_sh'

from itertools import izip
import numpy as np
import pylab
import Tools


def _GetPr( a_index, a_Bull ):
    if a_Bull:
        return _prsBull[a_index]
    else:
        return _prsBear[a_index]

_Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)
_prsBull, _prsBear = Tools.GetPrs(_Ls)

class Account:
    def __init__(self, a_cash):
        self.__cash = a_cash
        self.__dtVariety = {}
        self.__dtPrice = {} #记录Variety的当前价格
        self.__dtTime = {} #记录Variety的当前时间
        self.__dtLPos = {}
        self.__dtSPos = {}
        self.__vtDeals = []
        self.__margin = 0.0

    def AddContractInfo(self, a_name, a_multiplier, a_margin):
        self.__dtVariety[a_name] = (a_name, a_multiplier, a_margin)
        return

    def SetContractPrice(self, a_name, a_price, a_time):
        self.__dtPrice[a_name] = a_price
        self.__dtTime[a_name] = a_time

    def Open(self, a_name , a_count ):
        if a_count == 0:
            return False #不合逻辑的开仓
        if not self.__dtVariety.has_key(a_name):
            return False #没有这个Variety信息
        vi = self.__dtVariety[a_name]
        price = self.__dtPrice[a_name]
        time = self.__dtTime[a_name]
        c = abs(a_count)
        require = c*price*vi[1]*vi[2]
        if self.__cash < require:
            print u"Account: Oepn(%s,%s,%s) 可用资金不足 所需资金:%s 可用资金:%s" % (a_name,price,a_count,require,self.__cash)
            return False #可用资金不足
        self.__cash -= require
        if a_count > 0:
            pos = self.__dtLPos.get(a_name, [0,0])
            pos[0] = (pos[0]*pos[1] + price*c) / float(pos[1] + c) #仓位均价
            pos[1] = pos[1] + c #仓位数
            self.__dtLPos[a_name] = pos
            self.__vtDeals.append( {'Id':a_name,'Open':1,'Long':1,'Count':c,'Price':price,'Time':time} )
        else:
            pos = self.__dtSPos.get(a_name, [0,0])
            pos[0] = (pos[0]*pos[1] + price*c) / float(pos[1] + c) #仓位均价
            pos[1] = pos[1] + c #仓位数
            self.__dtSPos[a_name] = pos
            self.__vtDeals.append( {'Id':a_name,'Open':1,'Long':0,'Count':c,'Price':price,'Time':time} )
        return

    def Close(self, a_name, a_count):
        if a_count == 0:
            return False #不合逻辑的平仓
        if not self.__dtVariety.has_key(a_name):
            return False #没有这个Variety信息
        vi = self.__dtVariety[a_name]
        price = self.__dtPrice[a_name]
        time = self.__dtTime[a_name]
        c = abs(a_count)
        if a_count > 0:
            if not self.__dtLPos.has_key(a_name):
                return False #没有持仓信息
            if self.__dtLPos[a_name][1] < c:
                return False #没有足够的持仓可供Close
            pos = self.__dtLPos[a_name]
            pos[1] = pos[1] - c #仓位数
            self.__cash += pos[0]*c*vi[1]*vi[2] + (price-pos[0])*c*vi[1]
            self.__vtDeals.append( {'Id':a_name,'Open':0,'Long':1,'Count':c,'Price':price,'Time':time} )
        else:
            if not self.__dtSPos.has_key(a_name):
                return False #没有持仓信息
            if self.__dtSPos[a_name][1] < c:
                return False #没有足够的Short持仓可供Close
            pos = self.__dtSPos[a_name]
            pos[1] = pos[1] - c #仓位数
            self.__cash += pos[0]*c*vi[1]*vi[2] + (pos[0]-price)*c*vi[1]
            self.__vtDeals.append( {'Id':a_name,'Open':0,'Long':0,'Count':c,'Price':price,'Time':time} )
        return
    #获取动态权益
    def GetValue(self):
        value = self.__cash
        for name, posInfo in self.__dtLPos.iteritems():
            vi = self.__dtVariety[name]
            multiplier = vi[1]
            margin = vi[2]
            curPrice = self.__dtPrice[name]
            posPrice = posInfo[0]
            posCount = posInfo[1]
            value += posPrice*posCount*multiplier*margin + (curPrice-posPrice)*posCount*multiplier
        for name, posInfo in self.__dtSPos.iteritems():
            vi = self.__dtVariety[name]
            multiplier = vi[1]
            margin = vi[2]
            curPrice = self.__dtPrice[name]
            posPrice = posInfo[0]
            posCount = posInfo[1]
            value += posPrice*posCount*multiplier*margin + (posPrice-curPrice)*posCount*multiplier
        return value

    def GetDeals(self):
        return self.__vtDeals[:]

paras = Tools.GetCurrentParameters()
start = paras["start"]
end = paras["end"]
if0 = paras["if0"]
if1 = paras["if1"]
if0Multiplier = paras["multiplier0"]
if0Margin = paras["margin0"]
if1Multiplier = paras["multiplier1"]
if1Margin = paras["margin1"]

datas00 = Tools.GetDatas(if0, start, end, -1)[952:]
datas11 = Tools.GetDatas(if1, start, end, -1)[952:]

long = 0
short = 0
openBullTrd = 0.7
closeBullTrd = 0.4
openBearTrd = 0.7
closeBearTrd = 0.4
acc = Account(250000)
acc.AddContractInfo(if0, if0Multiplier, if0Margin)
acc.AddContractInfo(if1, if1Multiplier, if1Margin)

bullLY = []
bearLY = []

for i,ifps in enumerate(izip(datas00,datas11)):
    p0 = ifps[0]
    p1 = ifps[1]
    bullL = _GetPr(i, True)
    bearL = _GetPr(i, False)
    acc.SetContractPrice(if0, p0, i)
    acc.SetContractPrice(if1, p1, i)

    bullLY.append(bullL)
    bearLY.append(bearL)
    if bullL > openBullTrd:#开始牛市套利
        acc.Open(if0, 1)
        acc.Open(if1, -1)
    if bearL > closeBullTrd:#停止牛市套利
        acc.Close(if0, 1)
        acc.Close(if1, -1)
    if bearL > openBearTrd:#开始熊市套利
        acc.Open(if0, -1)
        acc.Open(if1,  1)
    if bullL > closeBearTrd: #停止熊市套利
        acc.Close(if0, -1)
        acc.Close(if1,  1)


print acc.GetValue()


x = np.array( [ i1-i0 for i0,i1 in izip(datas00,datas11)])


bullOpenX = []
bullOpenY = []
bullCloseX = []
bullCloseY = []


bearOpenX = []
bearOpenY = []
bearCloseX = []
bearCloseY = []

for d in  acc.GetDeals():
    if d["Id"] == if0:
        time = d["Time"]
        y = x[time]
        if d["Open"]  and d["Long"]:
            bullOpenX.append( time )
            bullOpenY.append( y )
        elif not d["Open"] and d["Long"]:
            bullCloseX.append( time )
            bullCloseY.append( y )
        elif d["Open"] and not d["Long"]:
            bearOpenX.append( time )
            bearOpenY.append( y )
        elif not d["Open"] and not d["Long"]:
            bearCloseX.append( time )
            bearCloseY.append( y )



fig = pylab.figure()
ax211 = fig.add_subplot(211)
ax211.plot(x, 'b-')

ax211.plot(bullOpenX, bullOpenY, 'rs' )
ax211.plot(bullCloseX, bullCloseY, 's' , mfc='none')

ax211.plot(bearOpenX, bearOpenY, 'go')
ax211.plot(bearCloseX, bearCloseY, 'o' , mfc='none')

ax212 = fig.add_subplot(212)
ax212.plot(bearLY, 'g-')
ax212.plot(bullLY, 'r-')

pylab.show()

