
import socket
import threading
import time

#addr = ('localhost', 33333)                                # localhost, port
#addr = ('127.0.0.1', 33333)                                # localhost explicitly
#addr = ('xyz', 33333)                                      # explicit computer
addr = '<broadcast>'                              # broadcast address
#addr = ('255.255.255.255', 33333)                          # broadcast address explicitly

class udpBroadcast(threading.Thread):
    def __init__(self, port):
        super(udpBroadcast, self).__init__()  
        self.port = port
        self.close = 0
        self.pause = 0
    def run(self):
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket
        self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.close == 0:
            try:
                if self.pause == 0: self.UDPSock.sendto("I am here", (addr, self.port))
                time.sleep(1)
            except:
                break

        self.UDPSock.close()             # Close socket
        print 'Broadcasting stopped.'

    def stop(self):
        self.close = 1
    def stopBroadcast(self):
        self.pause = 1
    def resumeBroadcast(self):
        self.pause = 0
