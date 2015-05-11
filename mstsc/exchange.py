# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
import time
import threading
from norlib.Socket.transfer import *

# 定义3个角色名称
# Client 远程连接 Target
# 由于Target不暴露在公网
# 通过Exchange做两者桥梁
# Client <=> ExchangeC <=> ExchangeT <=> Target


class Exchange(threading.Thread):
    def __init__(self, a_port, a_mstsc_internet_ip):
        threading.Thread.__init__(self)
        self.mstsc_internet_ip = a_mstsc_internet_ip
        self.exchange_ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exchange_ls.bind(('', a_port))
        self.exchange_ls.listen(5)
        self.peer0 = False
        self.peer1 = False
        self.__transfer0 = False
        self.__transfer1 = False

    def run(self):
        while True:
            s, address = self.exchange_ls.accept()
            if address == self.mstsc_internet_ip:
                if self.peer0:
                    print("来自mstsc的地址再次请求链接,关闭先前的链接")
                    self.peer0.close()
                self.peer0 = s
                print("Peer0 ", address)
                self.__transfer0 = Transfer(self.peer0, self.peer1, self._peer_closed, self)
                self.__transfer0.start()
                if self.__transfer1:
                    self.__transfer1.sink = s
                    print("建立通道")
            else:
                if self.peer1:
                    print("来自外部的地址要求链接mstsc,关闭先前连入mstsc的链接")
                    self.peer1.close()
                self.peer1 = s
                print("Peer1 ", address)
                self.__transfer1 = Transfer(self.peer1, self.peer0, self._peer_closed, self)
                self.__transfer1.start()
                if self.__transfer0:
                    self.__transfer0.sink = s
                    print("建立通道")

    @staticmethod
    def _peer_closed(a_exchange, a_peer):
        self = a_exchange
        if self.peer0 == a_peer:
            self.peer0 = False
            print("Peer0 关闭")
        elif self.peer1 == a_peer:
            self.peer1 = False
            print("Peer1 关闭")
        else:
            print("无法识别的Peer关闭:", a_peer)



if __name__ == '__main__':
    print('Start Exchange')
    #port = int(sys.argv[1])
    port = 6503
    Exchange(port).start()
