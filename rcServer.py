#!/usr/bin/python
# coding=utf-8

import threading
from threading import Thread
from time import sleep
import math

import RemoteControl.control
import RemoteControl.tcpServer
import RemoteControl.udpBroadcast
import RemoteControl.camera
from datetime import datetime

import sys
import subprocess
host = ''
port = 10369
streamPort = 10370
backlog = 5 
size = 4096
l = 0
r = 0
lastRequest = datetime.now()

running = 1

CameraThread = None
connectCnt = 0
udp = None

def CarControl():
    global lastRequest, l, r
    RemoteControl.control.CarSetup()
    try:
        print "Running Test Mode"
        RemoteControl.control.Test()
        print "Stopped Test Mode"
        while running == 1:
            if (datetime.now() - lastRequest).seconds > 2 :# stop the car if I cannot receive the signal in last 2 seconds
                l = 0
                r = 0
                lastRequest = datetime.now()
            RemoteControl.control.Move(l, r) # do not do thing now
            sleep(0.1)
        print "Car Stopped"
    finally:
        RemoteControl.control.Cleanup()



def eventHandler (command, message):
    global l, r, lastRequest
    global CameraThread, connectCnt
    if command == "Move":
        try:
            l = min(max(-127, int(message[:2], 16)-128), 127)
            r = min(max(-127, int(message[-2:], 16)-128), 127)
            lastRequest = datetime.now()
            print "Left", l, "Right", r 
        except ValueError: # drop packet if wrong format
            pass
    elif command == "Message":
        print "Display:", message
    elif command == "Shutdown":
        print "Shutdown now"
        subprocess.call(['shutdown -h now "System halted by Remote Car"'], shell=True)
    elif command == "Connected":
        print "Connected user"
        connectCnt +=1
        startCamera()
        print "already have client connected, stop broadcasting"
        udp.stopBroadcast()
    elif command == "Disconnected":
        print "Disconnected user"
        connectCnt -=1
        if connectCnt == 0:
            print "No active user, kill camera"
            stopCamera()
            print "No active user, start broadcasting"
            udp.resumeBroadcast()

        
def startCamera():
    global CameraThread
    if CameraThread is None:
        CameraThread = RemoteControl.camera.RaspiVidController(streamPort)
        CameraThread.start()
    
def stopCamera():
    global CameraThread
    if CameraThread is not None:
        print "Killing Cameara"
        CameraThread.stopController()
        CameraThread.join()
        print "Killed Cam?"
        CameraThread = None

def main():
    global running, udp
    print "Starting TCP Server"
    tcp = RemoteControl.tcpServer.tcpServer(eventHandler, host, port)
    tcp.start()
    udp = RemoteControl.udpBroadcast.udpBroadcast(port)
    udp.start()
    Thread(target=CarControl).start()
    while tcp.isAlive():
        try:
            tcp.join(1)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            running = 0
            stopCamera()
            udp.stop()
            tcp.stop()

     
if __name__ == '__main__':
    main()

