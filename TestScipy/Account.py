#coding: utf-8
__author__ = 'Administrator'


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