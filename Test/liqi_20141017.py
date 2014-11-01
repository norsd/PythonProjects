from datetime import datetime, timedelta
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import pylab

def drawBacktest(benchmarkReturn, portReturn, dailyDate):
    #pylab.plot_date(pylab.date2num(dailyDate),portReturn,'r',linewidth=0.8,linestyle='-')
    #pylab.plot_date(pylab.date2num(dailyDate),benchmarkReturn,'g',linewidth=0.8,linestyle='-')
    pylab.plot_date(dailyDate, portReturn,'r',linewidth=0.8,linestyle='-')
    xtext = pylab.xlabel('Out-Of-Sample Date')
    ytext = pylab.ylabel('Cumulative Return')
    ttext = pylab.title('Portfolio Return Vs Benchmark Return')
    pylab.grid(True)
    pylab.setp(ttext, size='large', color='r')
    pylab.setp(xtext, size='large', weight='bold', color='g')
    pylab.setp(ytext, size='large', weight='light', color='b')
    pylab.savefig('backtest.png')

benchmarkReturn = [0.1,0.2,0.3,0.4,0.5]
portReturn = [0.2,0.4,0.2,0.8,0.9]
today = datetime.now()
dailyDate = [today+timedelta(days=i) for i in range(5)]
drawBacktest(benchmarkReturn, portReturn, dailyDate)

yearsFmt = DateFormatter('%Y-%m-%d')
ax = pylab.gca()
ax.xaxis.set_major_formatter(yearsFmt)

pylab.show()