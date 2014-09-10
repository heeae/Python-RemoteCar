
import socket 
import re
class udpServer(threading.Thread):
    def run(self):
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((host, port))
        self.close = 0
        while self.close == 0:
            data, address = self.udpSocket.recvfrom(4) # a 2X 2byte hexString for left / right speed
            try:
                print "Left", int(data[:2], 16) - 128, "Right", int(data[-2:], 16) - 128
            except ValueError: # drop packet if wrong format
                pass
        print "UDP Server Stopped"

    def stop(self):
        print "UDP Server Stopping"
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto("XXXX",(host, port))
        self.udpSocket.close()
        self.close = 1
