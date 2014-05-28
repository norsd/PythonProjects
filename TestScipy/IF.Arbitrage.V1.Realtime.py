# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

from itertools import izip
from WindPy import w
import Account
import Arbitrage
import pylab
import time
import Tools


if0 = "IF1406.CFE"
if1 = "IF1407.CFE"
start = "2014-05-26 09:15:00"
end = "2014-05-27 15:15:00"
datasLen = len(Tools.GetDatas(if0, start, end, -1))
datasLen = len(Tools.GetDatas(if1, start, end, -1))

print "Datas Total Length:%s"%datasLen

if0Multiplier = 300
if1Multiplier = 300
if0Margin = 0.12
if1Margin = 0.12


sampleCount = int((4.5*60)*1)

Ls = (0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1,
      1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2)
deltaT = 5/float(245)


openBullTrd = 0.7
closeBullTrd = 0.4
openBearTrd = 0.7
closeBearTrd = 0.4

argsShow0 = []#保存用于显示价差以及回归的数据

datas0 = Tools.GetDatas2(if0, 0, sampleCount)
datas1 = Tools.GetDatas2(if1, 0, sampleCount)

print datas0[133],datas0[134],datas0[135]
print datas1[133],datas1[134],datas1[135]

a, b, sigmaEpsilon, muC, sigmaC, lns = Arbitrage.CreateParameters(datas0, datas1)

print "a=%s, b=%s, sigmaEpsilon=%s, mu=%s, sigma=%s" %(a, b, sigmaEpsilon, muC, sigmaC)


datas00 = Tools.GetDatas2(if0, sampleCount+2, sampleCount)
datas11 = Tools.GetDatas2(if1, sampleCount+2, sampleCount)
print datas00
print datas11
bullLs, bearLs = Arbitrage.CalculateD1D2(Ls, 0.4, a, b, sigmaEpsilon, muC, sigmaC, deltaT, datas00, datas11)


figure = pylab.figure()
pi = figure.add_subplot(211)
_dt = {}

line, = pi.plot( [], [], 'k-')

def OnTick(d):
    if not d.Codes[0] in _dt:
        _dt[d.Codes[0]] = []
    datas = _dt[d.Codes[0]]
    datas.append(d.Data[0][0])
    line.set_data(range(datas),datas)




w.start()
data = w.wsq("IF1406.CFE", "rt_last", func=OnTick)

pylab.show()

time.sleep(10)
Tools.ShowLinearAndPricesDelta(b, a, datas0, datas1)
