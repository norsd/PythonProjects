# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
from socket import error as SocketError
import errno
import time
import threading
from norlib.Socket.transfer import *
from norlib.Socket.Ip import *


class MstscServer(threading.Thread):
    def __init__(self, a_exchange_address, a_mstsc_ip, a_mstsc_port):
        threading.Thread.__init__(self)
        self.exchange_address = a_exchange_address
        self.exchange = False
        self.mstsc = False
        self.mstsc_ip = a_mstsc_ip
        self.mstsc_port = a_mstsc_port

    def run(self):
        while True:
            try:
                if not self.exchange:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(self.exchange_address)
                    self.exchange = s

                datas = self.exchange.recv(1024)
                if not datas:
                    print("远端链接关闭,准备关闭mstsc链接")
                    self.mstsc.close()
                    self.mstsc = False
                    self.exchange = False
                    continue
                if not self.mstsc:
                    print("建立mstsc")
                    self.mstsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.mstsc.connect((self.mstsc_ip, self.mstsc_port))
                    Transfer((self.mstsc, "mstsc"), (self.exchange, "exchange"), self._peer_closed, self).start()
                self.mstsc.send(datas)
                print("exchange=>mstsc")
            except SocketError as e:
                if e.errno == errno.ECONNRESET:
                    print("exchange 重置链接")
                    print("附带关闭mstsc")
                    self.mstsc.close()
                    self.mstsc = False
                    self.exchange = False
                    continue
            except:
                print("Unexpected error:", sys.exc_info())
                break

    @staticmethod
    def _peer_closed(a_exchange, a_peer):
        print("mstsc链接关闭!")
        print("关闭与exchange的链接")
        self = a_exchange
        self.exchange.close()
        self.exchange = False
        self.mstsc.close()
        self.mstsc = False

if __name__ == '__main__':

    exchange_ip = "101.95.130.218"
    exchange_port = 6503
    exchange_address = "101.95.130.218:6503"
    mstsc_ip = GetIps()[0]
    print('Start mstsc: ', mstsc_ip)
    mstsc_port = 3389
    MstscServer((exchange_ip, exchange_port), mstsc_ip, mstsc_port).start()