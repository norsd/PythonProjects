# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
import time
import threading


class Transfer(threading.Thread):
    def __init__(self, source, sink, fn, fn_para):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        self.fn_peer_closed = fn
        self.fn_peer_closed_para = fn_para

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:
                    self.fn_peer_closed(self.fn_peer_closed_para, self.source)
                self.sink.send(data)
            except:
                break