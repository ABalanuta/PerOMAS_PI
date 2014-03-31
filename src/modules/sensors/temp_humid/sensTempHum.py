#!/usr/bin/python

from time import sleep
from threading import Thread
from datetime import datetime
import subprocess
import os


#Temp and Humid Sensor Data Pin
dhtpin = 7


class TermoHumid(Thread):

    temp = 0.0
    humid = 0.0
    started = 0
    lastUpdate = 0
    executable = ""

    def __init__(self):
        self.stopped = False
        Thread.__init__(self)
        full_path = os.path.realpath(__file__)
        #self.executable = os.path.dirname(full_path)+"/aux/rpi_dht"
        self.executable = os.path.dirname(full_path)+"/aux/loldht"
        self.started = datetime.now()
        self.update()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.update()

    def update(self):
        values = subprocess.check_output([self.executable, str(dhtpin)])
        for line in values.split('\n'):
            if "Humidity" in line:
                #print str(datetime.now()), line
                parts = line.split(' ')
                #self.humid = parts[5]
                #self.temp = parts[9]
                self.humid = parts[2]
                self.temp = parts[6]
                self.lastUpdate = datetime.now()
                break

    def runtime(self):
        return str(self.lastUpdate-self.started).split(".")[0]

#Runs only if called
if __name__ == "__main__":

    started = datetime.now()

    print "#TEST#"
    print "#Starting#"
    d = TermoHumid()
    d.start()
    f = open('logging.log','a')

    while True:
        print "Runtime:", d.runtime(), "\tTemp:", d.temp, "\tHumid:", d.humid
        sleep(2)
        f.write(str(d.lastUpdate)+"\t"+"\tTemp:\t"+d.temp+"\tHumid:\t"+d.humid+"\n")
        f.flush()

    d.stop()
    f.close()
    print "#Sttoped#\n\n"
