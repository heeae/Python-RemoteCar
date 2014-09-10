
import time
import os
import subprocess
import threading
import signal

RASPIVIDCMD = "./mjpg-streamer/mjpg_streamer"
TIMETOWAITFORABORT = 0.5

#class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, port=10370):
        threading.Thread.__init__(self)
        
        #setup the raspivid cmd
        self.raspividcmd = [RASPIVIDCMD]

        #add file path, timeout and preview to options
        self.raspividcmd.append("-o")
        self.raspividcmd.append("./mjpg-streamer/output_http.so -w ./mjpg-streamer/nothing -p " + str(port))
        self.raspividcmd.append("-i")
        self.raspividcmd.append("./mjpg-streamer/input_raspicam.so -x 640 -y 480 -co 10 -br 60 -ISO 1600 -rot 180 -fps 12 -ex auto")


        #set state to not running
        self.running = False
        
    def run(self):
        #run raspivid
        self.running = True
        print "XXXXXXXXX", self.raspividcmd
        raspivid = subprocess.Popen(self.raspividcmd)
        
        #loop until its set to stopped or it stops
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False
        
        #kill raspivid if still running
        if raspivid.poll() is None: 
            raspivid.send_signal(signal.SIGINT) 
            while raspivid.poll() is None:
                time.sleep(TIMETOWAITFORABORT)
        print "Killed Camera"
        

    def stopController(self):
        self.running = False

