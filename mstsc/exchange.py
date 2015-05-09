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
    def __init__(self, a_port):
        threading.Thread.__init__(self)
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
            if not self.peer0:
                self.peer0 = s
                print("Peer0 ", address)
                self.__transfer0 = Transfer(self.peer0, self.peer1, self._peer_closed, self)
                self.__transfer0.start()
                if self.__transfer1:
                    self.__transfer1.sink = s
                    print("建立通道")
            elif not self.peer1:
                self.peer1 = s
                print("Peer1 ", address)
                self.__transfer1 = Transfer(self.peer1, self.peer0, self._peer_closed, self)
                self.__transfer1.start()
                if self.__transfer0:
                    self.__transfer0.sink = s
                    print("建立通道")
            else:
                s.close()
                print("Peer已经达到上限,新加入的Peer被拒绝:", address)

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
