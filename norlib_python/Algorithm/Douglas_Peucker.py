__author__ = 'Administrator'

import sys
import math
from decimal import *

def Compress(a_list,a_threshold,a_begin,a_end):
    vt = a_list
    b = a_begin
    e = a_end
    t = a_threshold
    if b>=e:
        raise 'Logical Error'
    elif b<0:
        raise  'Logical Error'
    elif e>=len(vt):
        raise 'Logical Error'

    if e-b <= 1 :#没有中间点就返回
        return
    else:
        (maxI,maxH) = _CalculateMax(vt,b,e)
        if  maxH<=t:#距离小于阈值
            #删除直线上所有点
            
        else:
            #保留该店
            #对该点的前后两段分别调用Compress


#计算首末点之间的点
#求垂直距离并找到距离最大值点
#[ , ]
def _CalculateMax(a_list,a_begin,a_end):
    vt = a_list
    b = a_begin
    e = a_end
    maxH=0
    maxI=-1
    a0 = a_list[b]
    a1 = a_list[e]
    for i in range(b+1,e):
        test = _CalculateMax( a0,a1,vt[i])
        if math.abs(test)>maxH:
            maxH = test
            maxI = i
    return (maxI,maxH)


def _CalculateVertical(a_ptA0,a_ptA1,a_ptB):
    a0 = a_ptA0
    a1 = a_ptA1
    b = a_ptB
    y = a1[1] - a0[1]
    x = a1[0] - a0[0]
    tg = Decimal(y)/x
    AB = ((b[1]-a[1])**2 + (b[0]-a[0])**2)**0.5
    S1 =  b[0]*tg
    S0 = b[1]-S1
    return math.cos( math.atg(tg))*S0

