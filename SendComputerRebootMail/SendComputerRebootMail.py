__author__ = 'di_shen_sh'
# coding=utf8
# 上句说明使用utf8编码

import sys
import inspect
import norlib_python.Mail.HtmlMail

#SendComputerRebootMail

if __name__ == "__main__":
    subject = u'计算机重启事件'
    content = u''
    norlib_python.Mail.HtmlMail.CreateHtmlMail(subject,html,content)