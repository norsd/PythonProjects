# -*- coding: utf-8 -*-

__author__ = 'norsd@163.com'

import sys
import socket
import time
import threading


class Transfer(threading.Thread):
    pipes = []
    pipeslock = threading.Lock()
    def __init__(self, source, sink, fn, fnpara):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        self.pipeslock.acquire()
        try:
            self.pipes.append(self)
        finally:
            self.pipeslock.release()
        self.pipeslock.acquire()
        try:
            pipes_now = len(self.pipes)
        finally:
            self.pipeslock.release()

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:
                    break
                self.sink.send(data)
            except:
                break
        self.sink.close()
        self.pipeslock.acquire()
        try:
            self.pipes.remove(self)
        finally:
            self.pipeslock.release()
        self.pipeslock.acquire()
        try:
            pipes_left = len(self.pipes)
        finally:
            self.pipeslock.release()