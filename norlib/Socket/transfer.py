# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
from socket import error as SocketError
import errno
import time
import threading


class Transfer(threading.Thread):
    def __init__(self, source, sink, fn, fn_para):
        threading.Thread.__init__(self)
        if source is tuple:
            self.source = source[0]
            self.sourcename = source[1]
        else:
            self.source = source
            self.sourcename = source.getpeername()

        if sink is tuple:
            self.sink = sink[0]
            self.sinkname = sink[1]
        else:
            self.sink = sink
            self.sinkname = "sink"
        self.fn_peer_closed = fn
        self.fn_peer_closed_para = fn_para

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:
                    self.fn_peer_closed(self.fn_peer_closed_para, self.source)
                    break
                elif not self.sink:
                    print("没有远端peer可以转发数据,数据被忽略")
                else:
                    self.sink.send(data)
                    print(self.sourcename, "=>", self.sinkname)
            except SocketError as e:
                if e.errno == errno.ECONNRESET:
                    self.fn_peer_closed(self.fn_peer_closed_para, self.source)
                    break
            except:
                print("Transfer ", self.source.getpeername(), " Unexpected error:", sys.exc_info())
                break