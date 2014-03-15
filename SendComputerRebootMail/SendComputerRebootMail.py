__author__ = 'di_shen_sh'
# coding=utf8
# 上句说明使用utf8编码

try:
    import os
    import sys
    import time
    #关键语句,使得py文件能够找到其他module
    #关键语句,使得py文件能够双击在外部运行
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from norlib_python.Mail import HtmlMail
    from norlib_python.Socket import Ip
except Exception,ex:
    print 'Load library Exception:\r\n'
    print ex
    os.system("pause")

#SendComputerRebootMail

if __name__ == "__main__":
    try:
        ips = Ip.GetIps()
        strIps = '<br/>'.join(ips)
        datetime = time.localtime(time.time())
        strDateTime = time.strftime('%Y-%m-%d %H:%M:%S',datetime)
        content = u'Info of Reboot Server<br/>DateTime:<br/>%s<br/>Ip:<br/>%s<br/>' % (strDateTime,strIps)
        subject = u'计算机重启事件'
        msg = HtmlMail.CreateMessage(subject,content)
        HtmlMail.Send("smtp.163.com","norsd_galaxy@163.com","norsd@Galaxy",msg,"norsd_galaxy@163.com","norsd_galaxy@163.com")
    except Exception,ex:
        print 'Exception:\r\n'
        print ex
    finally:
        os.system("pause")