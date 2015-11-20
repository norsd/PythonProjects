# coding: utf-8
import sys
import socket
import time
import threading

LOGGING = True
logLock = threading.Lock()


# 主功能类
# 此类一般用于内网机器通过一台有外网权限的内网服务器连接到外网
# 实现了数据的转发
# listen new_port
# 所有连接 new_port 和发往 new_port的数据都将转发到 ori_ip:ori_port
class Pinhole(threading.Thread):
    def __init__(self, a_new_port, a_ori_ip, a_ori_port):
        super(Pinhole, self).__init__()
        log('Redirecting:localhost:%s->%s:%s', a_new_port, a_ori_ip, a_ori_port)
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


def log(s, *a):
    if LOGGING:
        logLock.acquire()
        try:
            print('%s:%s' % (time.ctime(), (s % a)))
            sys.stdout.flush()
        finally:
            logLock.release()


# 继承自Thread
# 用于创建一条传递数据的通路
class PipeThread(threading.Thread):
    pipes = []
    pipesLock = threading.Lock()

    def __init__(self, source, sink):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        self.pipesLock.acquire()
        try:
            self.pipes.append(self)
        finally:
            self.pipesLock.release()
        self.pipesLock.acquire()
        try:
            pipes_now = len(self.pipes)
        finally:
            self.pipesLock.release()
        log('%s pipes now active', pipes_now)
        LockerDecorator(self).decorate()

    # Thread.run
    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:
                    break
                self.sink.send(data)
            except Exception as err:
                print("PipeThread线程发生异常:", err)
                break
        log('%s terminating (%s->%s)', self, self.source.getpeername() , self.sink.getpeername())
        self.sink.shutdown(socket.SHUT_RDWR)
        self.sink.close()
        self.source.close()
        self.pipesLock.acquire()
        try:
            self.pipes.remove(self)
        finally:
            self.pipesLock.release()
        self.pipesLock.acquire()
        try:
            pipes_left = len(self.pipes)
        finally:
            self.pipesLock.release()
        log('%s pipes still active', pipes_left)

    def close(self):
        self.source.shutdown(socket.SHUT_RDWR)
        self.source.close()
        self.pipes.remove(self)

    def __close_pair(self):
        self.Pair.Close()
        self.Pair = None


class DecorateClass(object):
    def decorate(self):
        for name, fn in self.iter():
            if not self.filter(name, fn):
                continue
            self.operate(name, fn)


class LockerDecorator(DecorateClass):
    def __init__(self, obj, lock= threading.RLock()):
        self.obj = obj
        self.lock = lock
    def iter(self):
        return [(name, getattr(self.obj, name)) for name in dir(self.obj)]
    def filter(self, name, fn):
        if not name.startswith('_') and callable(fn) and name[0].isupper():
              return True
        else:
              return False
    def operate(self, name, fn):
        def locker(*args, **kv):
            self.lock.acquire()
            try:
                return fn(*args, **kv)
            finally:
                self.lock.release()
        setattr(self.obj, name, locker)


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