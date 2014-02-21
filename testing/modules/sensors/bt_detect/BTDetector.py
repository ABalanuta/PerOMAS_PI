#!/usr/bin/python
import os
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime



class BTDetector(Thread):

    def __init__(self, hub):
		Thread.__init__(self)
		
		#Sudo required
		if os.geteuid() != 0:
			raise Exception("You need to have root privileges. Exiting.")
			
		self.stopped = False
		self.hub = hub
		
		p = subprocess.Popen('hciconfig -a', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		if not (len(lines) > 0 and "hci0" in lines[0]):
			raise Exception("No BT device Connected")
			
		subprocess.Popen('sudo hciconfig hci0 noscan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 name BT_$(hostname)', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 afhmode 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 sspmode 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 lm MASTER', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		

    def stop(self):
        self.stopped = True

    def run(self):
        print "Run not Implemented"

	def update(self):
		print "Update not Implemented"
		
	def registe_phone(self):
		print "Register not Implemented"
	
	def remove_phone(self):
		print "Remove not Implemented"
		


#Runs only if called
if __name__ == "__main__":

    started = datetime.now()

    print "#TEST#"
    print "#Starting#"
    d = BTDetector(None)
    
    
    
    print "#Sttoped#\n\n"
