#coding: utf-8
__author__ = 'di_shen_sh'

#根据数据库中的N(d1),N(d2) 找到每一个数据点的特定点L0,使得N(d1)*N(d2)为最大
#得到牛市和熊市套利的概率

from itertools import izip
import pylab
import Tools



Ls = (0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2)

datassBear = []
datassBull = []

ranksBull = []
lsBull = []
rankIndex = []
prTest = 0.5
for l in Ls:
    n1s, n2s = Tools.GetDNs(l, False)
    datassBull.append([n1*n2 for n1, n2 in izip(n1s, n2s)])


for j in range(0, len(datassBull[0])):
    row = [datassBull[i][j] for i in range(0, len(Ls))]
    ok = max(row)
    ranksBull.append(ok)
    rankIndex.append(row.index(ok))
    lsBull.append(Ls[row.index(ok)])

bull = [ rank for i,rank in enumerate(ranksBull) if rank>=prTest ]
print u'牛市:p>=%s , count:%s , ps:%s' %(prTest, len(bull), bull)


ranksBear = []
lsBear = []
rankIndex = []
for l in Ls:
    n1s, n2s = Tools.GetDNs(l, True)
    datassBear.append([n1*n2 for n1, n2 in izip(n1s, n2s)])

for j in range(0, len(datassBear[0])):
    row = [datassBear[i][j] for i in range(0, len(Ls))]
    ok = max(row)
    ranksBear.append(ok)
    rankIndex.append(row.index(ok))
    lsBear.append(Ls[row.index(ok)])

bear = [ rank for i,rank in enumerate(ranksBear) if rank>=prTest ]

print u'熊市:p>=%s , count:%s , ps:%s' %(prTest, len(bear), bear)

fig = pylab.figure()
plot0 = fig.add_subplot(221)
plot0.plot( [x*100 for x in ranksBull]  , '-' )
plot0.set_title('Bull')
pylab.ylabel(r'Percent [%]')
plot1 = fig.add_subplot(223)
plot1.plot( lsBull , '-')

plot2 = fig.add_subplot(222)
plot2.plot( [x*100 for x in ranksBear]  , 'g-' )
plot2.set_title('Bear')
plot3 = fig.add_subplot(224)
plot3.plot( lsBear , 'g-')


pylab.show()
