#coding: utf-8
__author__ = 'di_shen_sh'

#根据数据库中的N(d1),N(d2) 找到每一个数据点的特定点L0,使得N(d1)*N(d2)为最大


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


def _GetDNs( a_L ):
    collection = "L_%s" % (a_L)
    client = MongoClient('mongodb://localhost:27017/')
    col = client.Test[collection]
    n1 = [ x[u'N1'] for x in col.find()]
    n2 = [ x[u'N2'] for x in col.find()]
    return n1,n2

Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)

datass = []

for l in Ls:
    n1s,n2s = _GetDNs(l)
    datass.append( [ x[0]*x[1] for x in zip(n1s,n2s)] )


ranks = []
rankIndex= []
for j in range(0, len(datass[0])):
    row = [ datass[i][j] for i in range(0,len(Ls))]
    ok = max(row)
    ranks.append(ok)
    rankIndex.append( row.index(ok) )

print ranks
print rankIndex



