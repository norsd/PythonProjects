__author__ = 'di_shen_sh'
# coding=utf8
import re
import smtplib
import StringIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Header import Header

def CreateMessage(subject,htmlcontent):
    raw = u'''<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>CONTENT
</body>
</html>'''
    p = re.compile(r'([\w\W]+)CONTENT([\w\W]+)', re.UNICODE)
    html = p.sub(u'\1'+htmlcontent+u'\2',raw)
    msg = MIMEMultipart('alternative')
    msg['Subject']= Header(subject, charset='UTF-8')#中文主题
    #只能赋值一次
    #msg['From']= "From"
    #只能赋值一次
    #msg['To']='To'
    part1 = MIMEText(html,'html')
    msg.attach(part1)
    return msg

def Send(a_host,a_user,a_pass,a_msg,a_from,a_to):
    server = smtplib.SMTP()
    server.connect(a_host)
    server.login(a_user,a_pass)
    a_msg['From'] = a_from
    a_msg['To']= a_to
    server.sendmail(a_from,a_to,a_msg.as_string())
    server.quit()

if __name__ =="__main__":
    import smtplib
    #  注意 163       要求smtp的user和sender相匹配，否则无法投递
    mail_host = "smtp.163.com"
    mail_user= "norsd@163.com"
    mail_pass= "abcdefg"
    subject = "电脑重启!"
    content = u'这里是内容'
    message = CreateMessage(subject,'abcdefg')
    print message
    Send(mail_host,mail_user,mail_pass,message,"norsd@163.com","di_shen_sh@163.com")