import sys,socket,time,threading
LOGGING = True
logLock = threading.Lock()
def log(s,*a):
    if LOGGING:
        logLock.acquire()
        try:
            print '%s:%s' % (time.ctime(),(s%a))
            sys.stdout.flush()
        finally:
            logLock.release()


class PipeThread(threading.Thread):
    pipes = []
    pipesLock = threading.Lock()

    def __init__(self, source, sink):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink
        log('Creating new pipe thread %s (%s->%s)',
            self, source.getpeername(), sink.getpeername())
        self.pipesLock.acquire()
        try:self.pipes.append(self)
        finally:self.pipesLock.release()
        self.pipesLock.acquire()
        try:pipes_now = len(self.pipes)
        finally:self.pipesLock.release()
        log('%s pipes now active',pipes_now)

    #Thread.run
    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data:break
                self.sink.send(data)
            except:
                break
        log('%s terminating (%s->%s)',self , self.source.getpeername() , self.sink.getpeername())
        self.sink.close()
        self.source.close()
        self.pipesLock.acquire()
        try:
            self.pipes.remove(self)
        finally:
            self.pipesLock.release()
        self.pipesLock.acquire()
        try:pipes_left = len(self.pipes)
        finally:self.pipesLock.release()
        log('%s pipes still active',pipes_left)
    #Decorate Function
    def sync(func):
        def wrapper(*args, **kv):
            self = args[0]
            self.pipesLock.acquire()
            try:
                return func(*args,**kv)
            finally:
                self.pipesLock.release()
        return wrapper


    @sync
    def Close(self):
        self.source.close()
        self.pipes.remove(self)


    def __ClosePair(self):
        print self.Pair
        #if not self.Pair:
        self.Pair.Close()
        self.Pair = None



class Pinhole(threading.Thread):
    def __init__(self,newPort, oriIp, oriPort):
        super(Pinhole,self).__init__()
        log('Redirecting:localhost:%s->%s:%s',newPort,oriIp,oriPort)
        self.__newPort = newPort
        self.__oriIp = oriIp
        self.__oriPort = oriPort
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(('',newPort))
        self.sock.listen(5)
    def run(self):
        while True:
            newsock,address = self.sock.accept()
            log('Creating new session for %s:%s',*address)
            fwd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            fwd.connect((self.__oriIp,self.__oriPort))
            pth0 = PipeThread(newsock,fwd)#.start()
            pth1 = PipeThread(fwd,newsock)#.start()
            pth0.Pair = pth1
            pth1.Pair = pth0
            pth0.start()
            pth1.start()

if __name__ == '__main__':
    print 'Starting Pinhole port forwarder/redirector'
    import sys
    try:
        newPort = int(sys.argv[1])
        oriIp = sys.argv[2]
        try:oriPort = int(sys.argv[3])
        except IndexError:oriPort =newPort
    except(ValueError,IndexError):
        print 'Usage: %s newPort oriIp [oriPort]' % sys.argv[0]
        sys.exit(1)
    sys.stdout = open('pinhole.log','w')
    Pinhole(newPort,oriIp,oriPort).start()

