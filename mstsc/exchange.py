__author__ = 'norsd@163.com'

import sys, socket, time, threading

#定义3个角色名称
#Client 远程连接 Target
#由于Target不暴露在公网
#通过Exchange做两者桥梁
#Client <=> ExchangeC <=> ExchangeT <=> Target
# c <=> ec <=> et <=> t

class ExchangeC(threading.Thread):
    def __init__(self, a_port):
        self.ec_ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ec_ls.bind(('', a_port))
        self.ec_ls.listen(5)

    def run(self):
        while True:
            c2ec, address = self.ec_ls.accept()
            ec2et = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ec2et.connect(self.et_ip, self.et_port)
            Transfer(c2ec, ec2et).start()
            Transfer(ec2et, c2ec).start()


class ExchangeT(threading.Thread):
    def __init__(self, a_port):
        self.et_ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.et_ls.bind(('', a_port))
        self.et_ls.listen(5)

    def run(self):
        while True:
            ec2et, address = self.et_ls.accept()
            et2t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            et2t.connect(self.t_ip, self.t_port)
            Transfer(ec2et, et2t).start()
            Transfer(et2t, ec2et).start()


class Transfer(threading.Thread):
    pipes = []
    pipeslock = threading.Lock()
    def __init__(self, source, sink):
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