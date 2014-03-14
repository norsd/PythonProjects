__author__ = 'di_shen_sh'
# coding=utf8
import re
import smtplib
import StringIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Header import Header

def CreateMessage(subject,content,htmlcontent=""):
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
    msg['From']= "me"
    msg['To']='you'
    part0 = MIMEText(content, _subtype='plain',  _charset='UTF-8')
    part1 = MIMEText(html,'html')
    msg.attach(part0)
    msg.attach(part1)
    return msg

def Send(a_host,a_user,a_pass,a_msg,a_sender=""):
    server = smtplib.SMTP()
    server.connect(a_host)
    server.login(a_user,a_pass)
    server.sendmail(a_sender,a_sender,a_msg.as_string())
    server.quit()

if __name__=="__main__":
    import smtplib
    mail_host = "smtp.163.com"
    mail_user="di_shen_sh@163.com"#"norsd@163.com"
    mail_pass="123456"
    subject = "电脑重启!"
    content = u'这里是内容'
    message = CreateMessage(subject,content)
    Send(mail_host,mail_user,mail_pass,message,"di_shen_sh@163.com")