#!/usr/bin/env python
"""Bluetooth Detection Module

Detects bluetooth beacons sent from devices and stores for a shor period,
Invokes CLI commands and bluez python code.
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime

#Debbuging Mode
DEBUG = 1

class BTExecutor(Thread):
	
	#Return value
	value = None
	
	def __init__(self):
		Thread.__init__(self)
		#print "BTExecutor thread init"

	def run(self):
		p = subprocess.Popen('sudo bluez-test-discovery', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		
		found_name = []
		found_mac = []
		found_rssi = []
		
		#Find devices and their parameters
		for line in lines:
			if "Name" in line:
				if len(line.split()) > 2: #Name could be null
					found_name += [' '.join(line.split()[2:])]
				else:
					found_name += [""]
			if "Address" in line:
				found_mac += [line.split()[2]]
			if "RSSI" in line:
				found_rssi += [line.split()[2]]
		
		#Put device parameters in a dictionary
		found = []
		for x in range(0, len(found_name)):
			device = dict()
			device['Address'] = found_mac[x]
			device['Name'] = found_name[x]
			device['RSSI'] = found_rssi[x]
			device['Quality'] = int((int(found_rssi[x])+97)*1.325)
			
			#Filter duplicates
			for dev in found:
				if device['Address'] == dev['Address']:
					continue
			
			found.append(device)
		
		# make it the returning values
		self.value = found
	
class BTDetector(Thread):

	stopped = None
	hub = None
	last_updated = None
	seen_devices = list()
	seen_timeout = 30	# if device is not seen for x seconds it gets eliminated
	
	def __init__(self, hub):
		Thread.__init__(self)
		
		#Sudo required
		if os.geteuid() != 0:
			raise Exception("You need to have root privileges. Exiting.")
			
		self.stopped = False
		self.hub = hub
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.interface_fail = 0
		self.reset_interface()

	def stop(self):
		self.stopped = True
		sleep(3)
		
	def runtime(self):
		return str(self.last_update-self.started).split(".")[0]
	
	def run(self):
		
		while not self.stopped:
			
			if DEBUG:
				print "\n-----------------------------------"
				
			exe = BTExecutor()
			exe.start()
			exe.join(16)
			if exe.value:
				self.last_update = datetime.now()
				self.update_seen_list(exe.value)
					
				if DEBUG:
					print "Found: " 
					for f in self.seen_devices:
						for k, v in f.items():
							print "\t\t", k, ": ",  v
						print "\n"
			else:
				self.reset_interface()
				self.interface_fail += 1
				
			if DEBUG:	
				print "Runtime: "+ self.runtime()
				print "Last Update ", str(self.last_update).split(".")[0]
				print "Hardware Fails: ", self.interface_fail
				print "-----------------------------------\n"
	

	def update_seen_list(self, devices):
		
		time_now = datetime.now()
		new_list = list()
						
		#Appends the new discovered devices to the seen list
		for device in devices:
			
			#Filters duplicates
			duplicate = False
			for d in new_list:
				if device["Address"] == d["Address"]:
					duplicate = True
					break
			
			if not duplicate:
				device["Last seen"] = time_now	
				new_list.append(device)
		
		
		#Appends older devices that did not timmed out yet
		for seen in self.seen_devices:
			
			new_version = False
			for device in new_list:
				if device["Address"] == seen["Address"]:
					new_version = True
			
			if not new_version:
				if not (time_now - seen["Last seen"]).total_seconds() > self.seen_timeout:
					new_list.append(seen)
		
		self.seen_devices = new_list
		
		
	def reset_interface(self):
		if DEBUG:
			print "Reset_interface()"
		
		
		self.kill_mod()
		while True:
			p = subprocess.Popen('hciconfig -a', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			lines = p.stdout.readlines()
			if not (len(lines) > 0 and "hci0" in lines[0]):
				if DEBUG:
					print "Kill_bt_mod()"
				self.kill_mod()
			else:
				break

		subprocess.Popen('sudo hciconfig hci0 noscan', shell=True)
		subprocess.Popen('sudo hciconfig hci0 name BT_$(hostname)', shell=True)
		subprocess.Popen('sudo hciconfig hci0 afhmode 1', shell=True)
		subprocess.Popen('sudo hciconfig hci0 sspmode 0', shell=True)
		subprocess.Popen('sudo hciconfig hci0 lm MASTER', shell=True)
		sleep(1)

	def kill_mod(self):
		subprocess.Popen('sudo rmmod btusb', shell=True)
		sleep(1)
		subprocess.Popen('sudo modprobe btusb', shell=True)
		sleep(1)	
	def find_devices(self):		
		return self.seen_devices
					
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
		print "-----------------"
		for x in d.seen_devices:
			print x
		print "-----------------"
