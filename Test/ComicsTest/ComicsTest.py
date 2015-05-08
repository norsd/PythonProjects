__author__ = 'di_shen_sh@163.com'
from selenium import webdriver
import time


#import urllib
#import urllib.request as urllib2

#response = urllib2.urlopen('http://www.dm5.com/m168636/')
#html = response.read()


url = "http://www.dm5.com/m168636/"
driver = webdriver.Chrome()
driver.get(url)

time.sleep(10) # wait to load

