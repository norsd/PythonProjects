# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
import time
import threading
from norlib.Socket.transfer import *
from norlib.Socket.Ip import *


class MstscServer(threading.Thread):
    def __init__(self, a_exchange_address, a_mstsc_ip, a_mstsc_port):
        threading.Thread.__init__(self)
        self.exchange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exchange.connect(a_exchange_address)
        self.mstsc = False
        self.mstsc_ip = a_mstsc_ip
        self.mstsc_port = a_mstsc_port

    def run(self):
        while True:
            try:
                datas = self.exchange.recv(1024)
                if not datas:
                    print("远端链接关闭")
                    break
                if not self.mstsc:
                    print("建立mstsc")
                    self.mstsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.mstsc.connect((self.mstsc_ip, self.mstsc_port))
                    Transfer((self.mstsc, "mstsc"), (self.exchange, "exchange"), self._peer_closed, self).start()
                self.mstsc.send(datas)
                print("exchange=>mstsc")
            except:
                print("Unexpected error:", sys.exc_info())
                break

    @staticmethod
    def _peer_closed(a_exchange, a_peer):
        print("fuck!!")
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

    exchange_ip = "101.95.130.218"
    exchange_port = 6503
    exchange_address = "101.95.130.218:6503"
    mstsc_ip = GetIps()[0]
    print('Start mstsc: ', mstsc_ip)
    mstsc_port = 3389
    MstscServer((exchange_ip, exchange_port), mstsc_ip, mstsc_port).start()