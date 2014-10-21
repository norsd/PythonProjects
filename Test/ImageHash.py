#coding: utf-8
#2014.10.21
#Reference:
#http://www.cnblogs.com/technology/archive/2012/07/12/2588022.html
__author__ = 'di_shen_sh@163.com'


import Image
import ImageOps
from itertools import izip
import numpy

def gethash(a_img0Path, w, h):
    img0 = Image.open(a_img0Path)
    imgs0 = img0.resize((w, h), Image.BILINEAR)
    rgbs0 = numpy.array(imgs0)
    vt = []
    for w in rgbs0:
        #extend类似c#中的AddRange函数
        #append类似c#中的Add函数
        vt.extend([(a[0]*30 + a[1]*59 + a[2]*11)/100 for a in w])
    #计算平均灰度
    average = sum(vt)/len(vt)
    bits = [(i > average)*1 for i in vt]
    return bits

def compare(a_img0Path, a_img1Path, w, h):
    h0 = gethash(a_img0Path, w, h)
    h1 = gethash(a_img1Path, w, h)
    c = [ (int)(a==b) for a,b in izip(h0, h1)]
    return sum(c)/float(len(c))*100

print compare("D:/Downloads/114813.JPG", "D:/114813_test.JPG", 32, 64)
print compare("D:/Downloads/114813.JPG", "D:/test_different.JPG", 32, 64)

#img = Image.open("D:/Downloads/114813.JPG")
#imgSmall = img.resize((32, 64), Image.BILINEAR)
#imgSmall.format, imgSmall.size, imgSmall.mode
#vt = img.histogram()
#grayimg = ImageOps.grayscale(imgSmall)
#arr = numpy.array(grayimg)
#rgbs = numpy.array(imgSmall)
#vt = []
#for w in rgbs:
    #extend类似c#中的AddRange函数
    #append类似c#中的Add函数
#    vt.extend( [(a[0]*30 + a[1]*59 + a[2]*11)/100 for a in w])

#计算平均灰度
#average = sum(vt)/len(vt)
#chars = [(i>average)*1 for i in vt]




#imgSmall.save("d:/test.jpg")