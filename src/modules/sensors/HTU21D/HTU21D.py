#!/usr/bin/python
import os
import subprocess
from random import randint
from time import sleep
from threading import Thread
from datetime import datetime



class TempHumid(Thread):

    def __init__(self, hub):
		Thread.__init__(self)
		self.stopped = False
		self.hub = hub
		full_path = os.path.realpath(__file__)
		self.executable = os.path.dirname(full_path)+"/htu21d.python3.py"
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.temp = 0
		self.humid = 0
		self.update_interval = 3 # 3 sec
		self.update()# Runs one time
		
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.update()
#            sleep(self.update_interval)

    def update(self):
		p = subprocess.Popen('sudo python3 ' + self.executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		parts = p.stdout.readlines()[0].split()					
		self.temp = parts[1][:7]
		self.humid = parts[3][:7]
		self.last_update = datetime.now()
        
    def runtime(self):
        return str(self.last_update-self.started).split(".")[0]

#Runs only if called
if __name__ == "__main__":

    started = datetime.now()

    print "#TEST#"
    print "#Starting#"
    d = TempHumid(None)
    d.start()
    
    try:
		while True:
			print "Runtime:", d.runtime(), "\tTemp:", d.temp, "\tHumid:", d.humid
			sleep(1)
    except: 
		d.stop()
    
    print "#Sttoped#\n\n"
