__author__ = 'di_shen_sh'
# coding=utf8
# 上句说明使用utf8编码

import sys
import time

from norlib_python.Mail import HtmlMail
from norlib_python.Socket import Ip

#SendComputerRebootMail

if __name__ == "__main__":

    ips = Ip.GetIps()
    strIps = '<br/>'.join(ips)
    datetime = time.localtime(time.time())
    strDateTime = time.strftime('%Y-%m-%d %H:%M:%S',datetime)
    content = u'Info of Reboot Server<br/>DateTime:<br/>%s<br/>Ip:<br/>%s<br/>' % (strDateTime,strIps)
    subject = u'计算机重启事件'
    msg = HtmlMail.CreateMessage(subject,content)
    HtmlMail.Send("smtp.163.com","norsd_galaxy@163.com","norsd@Galaxy",msg,"norsd_galaxy@163.com","norsd_galaxy@163.com")