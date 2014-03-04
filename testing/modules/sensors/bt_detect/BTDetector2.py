#!/usr/bin/python
import os
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime

#Debbuging Mode
DEBUG = 1

class BTExecutor(Thread):
	
	value = None
	
	def __init__(self):
		Thread.__init__(self)
		print "BTExecutor thread init"

	def run(self):
		p = subprocess.Popen('sudo bluez-test-discovery', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		found = []
		for line in lines:
			#if "Name" in line:
			#	print line
			if "Address" in line:
				found += [line.split()[2]]
			#elif "RSSI" in line:
			#	print line
			
		self.value = found
	
class BTDetector(Thread):

	stopped = None
	hub = None
	paired_devices = None
	paired_status_maximum = 3 # timeout +- 15s
	last_updated = None
	inter_ping_delay = 3
	
	def __init__(self, hub):
		Thread.__init__(self)
		
		#Sudo required
		if os.geteuid() != 0:
			raise Exception("You need to have root privileges. Exiting.")
			
		self.stopped = False
		self.hub = hub
		self.started = datetime.now()
		self.last_update = datetime.now()
		
		self.reset_interface()

	def stop(self):
		self.stopped = True
		sleep(3)
		
	def runtime(self):
		return str(self.last_update-self.started).split(".")[0]
	
	def run(self):
		
		fail = 0
		
		while not self.stopped:
			print "\n-----------------------------------"
			exe = BTExecutor()
			exe.start()
			exe.join(30)
			if exe.value:
				self.last_update = datetime.now()
				print "Found: ", exe.value
			else:
				self.reset_interface()
				fail += 1
				
			print "Runtime: "+ self.runtime()
			print "Last Update ", str(self.last_update).split(".")[0]
			print "Hardware Fails: ", fail
			print "-----------------------------------\n"
			
	def reset_interface(self):
		if DEBUG:
			print "Reset_interface()"
			
		subprocess.Popen('sudo rmmod btusb', shell=True)
		sleep(0.5)
		subprocess.Popen('sudo modprobe btusb', shell=True)
		sleep(1)
			
		p = subprocess.Popen('hciconfig -a', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		if not (len(lines) > 0 and "hci0" in lines[0]):
			raise Exception("No BT device Connected")
		
		subprocess.Popen('sudo hciconfig hci0 reset', shell=True)
		sleep(0.5)
		subprocess.Popen('sudo hciconfig hci0 noscan', shell=True)
		subprocess.Popen('sudo hciconfig hci0 name BT_$(hostname)', shell=True)
		subprocess.Popen('sudo hciconfig hci0 afhmode 1', shell=True)
		subprocess.Popen('sudo hciconfig hci0 sspmode 0', shell=True)
		subprocess.Popen('sudo hciconfig hci0 lm MASTER', shell=True)
		sleep(0.5)
			
#Runs only if called
if __name__ == "__main__":

	started = datetime.now()
	try:
		print "#TEST#"
		print "#Starting#"
		d = BTDetector(None)
		#print d.register_phone('40:B0:FA:3D:5F:08', '0000')
		#print d.register_phone('AC:81:F3:F6:FD:F7', '0001')
	
		#print d.get_paired()
		#print d.l2ping('AC:81:F3:F6:FD:F7')
		d.start()
		sleep(60*60*24*356)
		
	except:
		print "Exception"
	finally:
		d.stop()
		print "#Sttoped#\n\n"
