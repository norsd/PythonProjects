# coding: utf-8
import errno
import sys
import socket
import time
import threading
from norlib.Socket.Ip import *


# 主功能类
# 此类一般用于内网机器通过一台有外网权限的内网服务器连接到外网
# 实现了数据的转发
# listen new_port
# 所有连接 new_port 和发往 new_port的数据都将转发到 ori_ip:ori_port
class Pinhole(threading.Thread):
    def __init__(self, a_new_port, a_ori_ip, a_ori_port):
        super(Pinhole, self).__init__()
        log('Redirecting: localhost:%s -> %s:%s', a_new_port, a_ori_ip, a_ori_port)
        self.__newPort = a_new_port
        self.__oriIp = a_ori_ip
        self.__oriPort = a_ori_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', a_new_port))
        self.sock.listen(5)

    # 打开双向通道
    def run(self):
        while True:
            # 获取一个连接到 new_port 的连接
            # new_port_sock 是连接到new_port的连接(一般来自内网)
            new_port_sock, address = self.sock.accept()
            log('Creating new session for %s:%s', *address)
            ori_port_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ori_port_sock.connect((self.__oriIp, self.__oriPort))
            # new_port_sock收到的数据 发送到 ori_port_sock(外网）
            pth0 = PipeThread(new_port_sock, ori_port_sock)
            # ori_port_sock发来的数据 发送到 new_port_sock(内网机器)
            pth1 = PipeThread(ori_port_sock, new_port_sock)
            pth0.Pair = pth1
            pth1.Pair = pth0
            pth0.start()
            pth1.start()


# 继承自Thread
# 用于创建一条传递数据的通路
# source.recv 得到数据后
# sink.send 将数据推送给外部
class PipeThread(threading.Thread):
    pipes = []
    pipesLock = threading.Lock()
    _source_ipport = ""
    _target_ipport = ""
    _closed = False

    def __init__(self, source, sink):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        self._source_ipport = get_address_string(source)
        self._target_ipport = get_address_string(sink)
        self.pipesLock.acquire()
        log('%s 创建', self)
        try:
            self.pipes.append(self)
            log('%s 的pipes长度为 %s', self, len(self.pipes))
        finally:
            self.pipesLock.release()
        self.pipesLock.acquire()
        try:
            pipes_now = len(self.pipes)
        finally:
            self.pipesLock.release()
        log('%s pipes now active', pipes_now)       

    def __str__(self):
        return "( %s -> %s )" % (self._source_ipport, self._target_ipport)

    # Thread.run
    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:
                    break
            except socket.error as error:
                if error.errno == errno.WSAECONNRESET:
                    log('Source Socket(%s) 重置', self._source_ipport)
                    break
            except Exception as err:
                log('Source Socket(%s) 异常: %s', err)
            try:
                self.sink.send(data)
            except Exception as err:
                log("Target Socket(%s) Send异常: %s", self._target_ipport, err)
                break
        log('%s 关闭中', self)
        self.sink.close()
        self.source.close()
        # 原子操作
        self.pipesLock.acquire()
        try:
            self._closed = True
            self.pipes.remove(self)
            pipes_left = len(self.pipes)
        finally:
            self.pipesLock.release()
        # 原子操作结束
        log('%s 已经关闭', self)
        log('%s pipes still active', pipes_left)


def log(s, *a):
        logLock.acquire()
        try:
            print('%s:%s' % (time.ctime(), (s % a)))
            sys.stdout.flush()
        finally:
            logLock.release()


# log函数的全局锁
logLock = threading.Lock()
# main函数
if __name__ == '__main__':
    print('Starting Pinhole')
    import sys
    try:
        newPort = int(sys.argv[1])
        oriIp = sys.argv[2]
        try:
            oriPort = int(sys.argv[3])
        except IndexError:
            oriPort = newPort
    except(ValueError, IndexError):
        print('Usage: %s newPort oriIp [oriPort]' % sys.argv[0])
        sys.exit(1)
    Pinhole(newPort, oriIp, oriPort).start()