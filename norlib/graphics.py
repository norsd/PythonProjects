__author__ = 'di_shen_sh@163.com'

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#bar图
class bar:
    #默认正数显示红色,负数显示绿色
    #a_datas是数值型集合
    #xinfos_fn是可以通过双击Bar在Console中显示出相应的信息,例如时间信息序列
    #xinfos_fn也可以是一个形如Action<int>的回调函数,参数0表示当前被点击的Bar的Index
    def draw(a_datas, a_xinfos_fn=None, positive='red', negative='green'):
        y = a_datas

        xp = [i for i in range(0, len(y)) if y[i]>=0]
        yp = [y[i] for i in xp]

        xn = [i for i in range(0, len(y)) if y[i]<0]
        yn = [y[i] for i in xn]

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.bar(xp, yp, 0.35, color=positive, picker=a_xinfos_fn is not None)
        ax1.bar(xn, yn, 0.35, color=negative, picker=a_xinfos_fn is not None)

        if a_xinfos_fn is not None:
            #创建回调函数
            if callable(a_xinfos_fn):
                action = a_xinfos_fn
            else:
                def tmp(a_index):
                    print(a_xinfos_fn[a_index])
                action = tmp
            for label in ax1.get_xticklabels():  # make the xtick labels pickable
                label.set_picker(True)
            #定义闭包函数
            def _onpick1(event):
                if isinstance(event.artist, Rectangle):
                    rect = event.artist
                    #matplotlib中Rectangle的x就是index
                    index = rect.get_x()
                    action(index)
            fig.canvas.mpl_connect('pick_event', _onpick1)
        plt.show()
        return


    def sample():
        N = 5
        menMeans   = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd     = (2, 3, 4, 1, 2)
        womenStd   = (3, 5, 2, 3, 3)
        ind = np.arange(N)    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, menMeans,   width, color='r', yerr=womenStd)
        p2 = plt.bar(ind, womenMeans, width, color='y',
                     bottom=menMeans, yerr=menStd)

        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
        plt.yticks(np.arange(0,81,10))
        plt.legend( (p1[0], p2[0]), ('Men', 'Women') )

        plt.show()



#直方图(正态分布)
class hist:
    def draw(a_x, a_countOfbins=50):
        plt.hist(a_x, a_countOfbins, normed=1, facecolor='green', alpha=0.5)
        plt.show()
        return

    #直接运行显示一个实例
    def sample():
        """
        Demo of the histogram (hist) function with a few features.

        In addition to the basic histogram, this demo shows a few optional features:

            * Setting the number of data bins
            * The ``normed`` flag, which normalizes bin heights so that the integral of
              the histogram is 1. The resulting histogram is a probability density.
            * Setting the face color of the bars
            * Setting the opacity (alpha value).

        """

        # example data
        mu = 100 # mean of distribution
        sigma = 15 # standard deviation of distribution
        x = mu + sigma * np.random.randn(10000)

        num_bins = 50
        # the histogram of the data
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Smarts')
        plt.ylabel('Probability')
        plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.show()


class xcorr:
    def draw(a_x, a_y = None):
        x = a_x
        y = a_y
        if a_y is None:
            y = [i for i in range(0, len(x))]
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        #ax1.xcorr(x, y, usevlines=True, normed=True, lw=2)
        ax1.xcorr(x, y)
        ax1.grid(True)
        #ax1.axhline(0, color='black', lw=2)
        plt.show()

