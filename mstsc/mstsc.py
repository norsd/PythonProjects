# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
import time
import threading
from norlib.Socket.transfer import *


class MstscServer(threading.Thread):
    def __init__(self, a_exchange_ip, a_exchange_port, a_mstsc_ip, a_mstsc_port):
        self.exchange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exchange.connect(a_exchange_ip, a_exchange_port)
        self.mstsc = False
        self.mstsc_ip = a_mstsc_ip
        self.mstsc_port = a_mstsc_port

    def run(self):
        while True:
            try:
                datas = self.exchange.recv(1024)
                if not self.mstsc:
                    self.mstsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.mstsc.connect(self.mstsc_ip, self.mstsc_port)
                    Transfer(self.mstsc, self.exchange)
                self.mstsc.send(datas)
            except:
                print("Unexpected error:", sys.exc_info()[0])
