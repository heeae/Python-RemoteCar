import threading
from threading import Thread
import socket 
import re


class tcpServer(threading.Thread):
    def __init__(self, event = None, host = '', port = 10369):
        super(tcpServer, self).__init__()
        self.host = host
        self.port = port
        self.event = event

    def run(self):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((self.host, self.port))
        self.tcpSocket.listen(5)
        self.close = 0
        while self.close == 0:
            client, address = self.tcpSocket.accept()
            print "Client from " + repr(address) + " is connected"
            if self.event is not None:
                self.event("Connected", (client, address))
            Thread(target=self.process, args=(client, address,)).start()
        print "Server Stopped"
            
    def process(self, client, address):
        pattern = re.compile("<([a-zA-Z0-9_]+)>([^\[]+)\[end\]", re.M | re.U)
        msg = ""
        while self.close == 0:
            try:
                msg += client.recv(10)
            except:
                break
            if not msg: break
                # look for start Tag  
            m = pattern.search(msg);
            if m:
                client.send("OK\r\n")
                if self.event is not None:
                    self.event( m.group(1), m.group(2))
                msg = msg[m.span()[1]:]
        print "Client from " + repr(address) + " is disconnected"
        if self.event is not None:
            self.event("Disconnected", (client, address))

    def stop(self):
        print "Server Stopping"
        self.event = None # stop propagate event
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect( (self.host, self.port))
        self.tcpSocket.shutdown(socket.SHUT_RDWR);
        self.tcpSocket.close()
        self.close = 1


