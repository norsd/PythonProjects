__author__ = 'Administrator'
import socket
import matplotlib.pyplot as plt
import thread
import re
import string

SHOW_DURATION = 100 # duration of X
Y_MAX = 1000
Y_MIN = -1000

# Init Socket for Receiving
address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)


# Main Loop
def Loop():
    audio = [0]*300
    video = [0]*300
    diff = [0]*300
    reobj = re.compile(r"Audio PTS = ([\d]*), Video PTS = ([\d]*)")
    cnt = 0 # recv counter
    plt.hold(False)# Hold Off
    while True:
        # Receive Data form Socket
        print 1
        data, addr = s.recvfrom(2048)
        print 1
        cnt += 1
        # Parse the Data
        match = reobj.search(data)
        if match:
            curAudio = string.atol(match.group(1))
            curVideo = string.atol(match.group(2))
            audio += [curAudio]
            video += [curVideo]
            diff += [curAudio - curVideo]
        # Plot the figure every 15 packets received if we plot too frequently, it will block the new packet
        if(0 == cnt%15):
            iStart = len(diff) - SHOW_DURATION
            if iStart < 0:
                iStart = 0
            # plot the data
            plt.plot(x[iStart:-1],diff[iStart:-1])
            # To set the limit of y, ylim() should be called after plot, or it will lose efficacy
            plt.ylim(Y_MIN, Y_MAX)
            # to refresh the figure by force
            plt.draw()


# Thread for Receiving Data from Socket
thread.start_new_thread(Loop,())

# show UI
plt.show()

s.close()
