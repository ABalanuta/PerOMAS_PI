#!/usr/bin/python
import os
import subprocess
from random import randint
from time import sleep
from threading import Thread
from datetime import datetime



class TempHumidFake(Thread):

    def __init__(self, hub):
		Thread.__init__(self)
		self.stopped = False
		self.hub = hub
		full_path = os.path.realpath(__file__)
		self.executable = os.path.dirname(full_path)+"/aux/rht03"
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.temp = 0
		self.humid = 0
		self.update()# Runs one time
		
    def stop(self):
        self.stopped = True
        subprocess.Popen('sudo killall rht03', shell=True) # kills the process

    def run(self):
        while not self.stopped:
            self.update()

    def update(self):
		p = subprocess.Popen(
							self.executable, shell=True,
							stdout=subprocess.PIPE)
		for line in p.stdout.readlines():
			if "Temp" in line:
				parts = line.split()
				self.humid = parts[1]
				self.temp = parts[3]
				self.last_update = datetime.now()
        
    def runtime(self):
        return str(self.last_update-self.started).split(".")[0]

#Runs only if called
if __name__ == "__main__":

    started = datetime.now()

    print "#TEST#"
    print "#Starting#"
    d = TempHumidFake(None)
    d.start()
    try:
		while True:
			print "Runtime:", d.runtime(), "\tTemp:", d.temp, "\tHumid:", d.humid
			sleep(1)
    except: 
		d.stop()
    
    print "#Sttoped#\n\n"
