__author__ = 'Administrator'
# coding=utf8

import socket

def GetIps():
    # 根据hostname获取一个主机关于IP和名称的全面的信息。
    # 返回主机名,主机别名列表,主机IP地址列表
    infos = socket.gethostbyname_ex(socket.gethostname())
    return  infos[2]