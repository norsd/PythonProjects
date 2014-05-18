# -*- coding: utf-8 -*-
__author__ = 'di_shen_sh'

from scipy import stats
import Arbitrage
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import Tools

if0 = "IF1311.CFE"
if1 = "IF1312.CFE"
start = "2013-10-10 09:00:00"
end = "2013-11-10 15:00:00"

sampleCount = int((4.5*60)*5)
tradeCount = int((4.5*60)*5)

Tools.GetDatas(if0, start, end, 1)
Tools.GetDatas(if1, start, end, 1)

for i in range(0, 3):
    datas0 = Tools.GetDatas2(if0, i*tradeCount, sampleCount)
    datas1 = Tools.GetDatas2(if1, i*tradeCount, sampleCount)
    a, b, sigmaEpsilon, muC, sigmaC, lns = Arbitrage.CreateParameters(datas0, datas1)
    #Tools.Show0(if0, if1, start, datas0, datas1, a, b, lns)
    ls = Arbitrage.CalculateL
    #income