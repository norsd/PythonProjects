# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

from itertools import izip
import Account
import Arbitrage
import Tools

key = 'now'
key = 'last'
if key == 'now':
    if1 = "IF1406.CFE"
    if0 = "IF1407.CFE"
    start = "2014-05-19 09:15:00"#"2013-10-19 09:00:00"
    end = "2014-05-23 15:15:00"
if key == 'last':
    if1 = "IF1405.CFE"
    if0 = "IF1406.CFE"
    start = "2014-04-21 09:15:00"#"2013-10-19 09:00:00"
    end = "2014-05-16 15:15:00"

if0Multiplier = 300
if1Multiplier = 300
if0Margin = 0.12
if1Margin = 0.12


sampleCount = int((4.5*60)*1)
tradeCount = int((4.5*60)*1)

datasLen = len(Tools.GetDatas(if0, start, end, -1))
datasLen = len(Tools.GetDatas(if1, start, end, -1))


print "Datas Length: %s" % datasLen

Ls = (0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1,
      1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2)
deltaT = 5/float(245)

acc = Account.Account(250000)
acc.AddContractInfo(if0, if0Multiplier, if0Margin)
acc.AddContractInfo(if1, if1Multiplier, if1Margin)

openBullTrd = 0.7
closeBullTrd = 0.4
openBearTrd = 0.7
closeBearTrd = 0.4

argsShow0 = []#保存用于显示价差以及回归的数据

i=0
while i < (datasLen/sampleCount):
    datas0 = Tools.GetDatas2(if0, i*tradeCount, sampleCount)
    datas1 = Tools.GetDatas2(if1, i*tradeCount, sampleCount)
    datas00 = Tools.GetDatas2(if0, i*tradeCount+sampleCount, tradeCount)
    datas11 = Tools.GetDatas2(if1, i*tradeCount+sampleCount, tradeCount)
    print len(datas0),len(datas1)
    a, b, sigmaEpsilon, muC, sigmaC, lns = Arbitrage.CreateParameters(datas0, datas1)
    if b==1:
        ifTmp = if0
        if0 = if1
        if1 = ifTmp
        continue
    print "a=%s, b=%s, sigmaEpsilon=%s, mu=%s, sigma=%s" %(a, b, sigmaEpsilon, muC, sigmaC)
    bullLs, bearLs = \
        Arbitrage.CalculateD1D2(Ls, 0.4, a, b, sigmaEpsilon, muC, sigmaC, deltaT, datas00, datas11)

    #Trade
    si = len(datas0)
    if abs(a) > 500:
        print "ignore!!!!!!!!!!!!!!!!"
    else:
        pos = 0
        for j, ifps in enumerate(izip(datas00, datas11)):
            p0 = ifps[0]
            p1 = ifps[1]
            bullL = bullLs[j]
            bearL = bearLs[j]
            acc.SetContractPrice(if0, p0, si+j)
            acc.SetContractPrice(if1, p1, si+j)
            if bullL > openBullTrd and pos == 0:#开始牛市套利
                acc.Open(if0, 1)
                acc.Open(if1, -1)
                pos = 1
            if bearL > closeBullTrd and pos == 1:#停止牛市套利
                acc.Close(if0, 1)
                acc.Close(if1, -1)
                pos = 0
            if bearL > openBearTrd and pos == 0:#开始熊市套利
                acc.Open(if0, -1)
                acc.Open(if1,  1)
                pos = -1
            if bullL > closeBearTrd and pos == -1: #停止熊市套利
                acc.Close(if0, -1)
                acc.Close(if1,  1)
                pos = 0
        acc.Close(if0, 1)
        acc.Close(if0, -1)
        acc.Close(if1, 1)
        acc.Close(if1, -1)
        print acc.GetValue()
    #保存用于显示价差以及回归的数据
    argsShow0.append((datas0, datas1, a, b, datas00, datas11))
    i += 1

#记录交易点
bullOpenX = []
bullCloseX = []
bearOpenX = []
bearCloseX = []

for d in acc.GetDeals():
    if d["Id"] == if0:
        time = d["Time"]
        if d["Open"] and d["Long"]:
            bullOpenX.append(time)
        elif not d["Open"] and d["Long"]:
            bullCloseX.append(time)
        elif d["Open"] and not d["Long"]:
            bearOpenX.append(time)
        elif not d["Open"] and not d["Long"]:
            bearCloseX.append(time)

Tools.Show0(if0, if1, start, argsShow0, (bullOpenX, bullCloseX),
                                        (bearOpenX, bearCloseX))

print acc.GetValue()