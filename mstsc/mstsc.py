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
        # socket error count
        serr_cnt = 0
        # 超过serr_max之后开始休眠
        serr_max = 5
        # 休眠3秒
        slp_sec = 3
        rok = False
        transfer = False
        while True:
            try:
                if not self.exchange:
                    if serr_cnt >= serr_max:
                        print("错误数超过", serr_max, "休眠", slp_sec)
                        time.sleep(slp_sec)
                    print("准备连接 exchange")
                    # 表示是否接受到过数据
                    rok = False
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(self.exchange_address)
                    s.settimeout(20.0)
                    self.exchange = s
                    serr_cnt = 0
                    print("已连接 exchange")
                datas = self.exchange.recv(1024)
                if not datas:
                    print("远端链接关闭,准备关闭mstsc链接")
                    if not self.mstsc:
                        # self.mstsc已经成为了False
                        zero = 0
                    else:
                        self.mstsc.close()
                        self.mstsc = False
                    # 设置exchange = False准备下次链接
                    self.exchange = False
                    print("已关闭mstsc链接")
                    continue
                if not rok:
                    rok = True
                    print("与exchange的连接已经收到数据")
                if not self.mstsc:
                    print("建立mstsc")
                    self.mstsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.mstsc.connect((self.mstsc_ip, self.mstsc_port))
                    if transfer:
                        transfer.Close = True
                    transfer = Transfer((self.mstsc, "mstsc"), (self.exchange, "exchange"), self._peer_closed, self)
                    transfer.start()
                self.mstsc.send(datas)
            except socket.timeout:
                if rok:
                    continue
                else:
                    print("exchange 长时间没有数据发送,中止随后重新连接")
                    self.exchange.close()
                    self.exchange = False
                    continue
            except SocketError as e:
                serr_cnt += 1
                if e.errno == errno.ECONNRESET:
                    print("exchange 重置链接")
                    if self.mstsc:
                        print("附带关闭mstsc")
                        self.mstsc.close()
                        self.mstsc = False
                    self.exchange = False
                    continue
                elif e.errno == errno.ECONNABORTED:
                    print("exchange 你的主机中的软件中止了连接")
                    if self.mstsc:
                        print("附带关闭mstsc")
                        self.mstsc.close()
                        self.mstsc = False
                    self.exchange = False
                    continue
                elif e.errno == errno.ECONNREFUSED:
                    print("exchange 计算机积极拒绝")
                    continue
                elif e.errno == errno.ETIMEDOUT:
                    print("exchange 连接超时")
                    continue
                elif e.errno == errno.ENOTSOCK:
                    print("exchange 非法套接字操作, 可能是要求一个已经关闭的套接字发送数据:", sys.exc_info())
                    # 发生这个异常可能是mstsc自动关闭(有外部新连接mstsc,所以老连接被关闭)后
                    # exchange有消息收到后转发mstsc发生此异常
                    # 我们等待3秒后,检查self.exchange与self.mstsc是否已被_peer_closed函数重置
                    time.sleep(3)
                    if not self.exchange and not self.mstsc:
                        continue
                    else:
                        print("exchange 非法套接字操作发生3秒后, 相关变量仍然没有被重置, 服务中止")
                        break

                else:
                    print("其他SocketError:", e, " No.:", e.errno)
                    print("无法处理此错误,中断服务")
                    break
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