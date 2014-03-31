#!/usr/bin/python
import os
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime

#Debbuging Mode
DEBUG = 1

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
		self.paired_devices = dict()
		self.last_updated = datetime.now()
		
		p = subprocess.Popen('hciconfig -a', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		if not (len(lines) > 0 and "hci0" in lines[0]):
			raise Exception("No BT device Connected")
		
		#Configures the Interface
		subprocess.Popen('sudo hciconfig hci0 reset', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 noscan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 name BT_$(hostname)', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 afhmode 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 sspmode 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		subprocess.Popen('sudo hciconfig hci0 lm MASTER', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		#Get Pared Devices
		self.renew_paired_list()

	def register_phone(self, mac, pin):
		
		mac = mac.upper()
		
		
		#removes first if already paired
		if mac in self.paired_devices.keys():
			self.remove_phone(mac)
		
		p = subprocess.Popen('echo '+pin+' | sudo bluez-simple-agent hci0 '+mac, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		if len(lines) == 3 and "New device" in lines[2]:
			subprocess.Popen('sudo bluez-test-device trusted '+mac+' yes', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			self.paired_devices[mac] = 0
			return "Pair OK"
		else:
			return "Pair Fail"

	def remove_phone(self, mac):
		subprocess.Popen('sudo bluez-test-device remove '+mac, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	def renew_paired_list(self):
		p = subprocess.Popen('sudo bluez-test-device list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		for line in lines:
			found_mac = line.split()[0]
			self.paired_devices[found_mac] = 0 # inicialize at zero

	def stop(self):
		self.stopped = True
		sleep(3)
	
	def l2ping(self, mac):
		p = subprocess.Popen('sudo l2ping '+mac+' -s 0 -c 1',
							shell=True,
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT)
		lines = p.stdout.readlines()
		if DEBUG:
			print lines
		
		if len(lines) == 3 and mac in lines[1] and '1 received' in lines[2]:
			sleep(self.inter_ping_delay)
			return 1
		elif len(lines) == 1 and 'Host is down' in lines[0]:
			sleep(1)
			return -1
		else:
			
			if self.stopped:
				return
				
			print "Interface Error"
			self.reset_interface()
			return self.l2ping(mac)
			
	def run(self):
		count  = 0 
		while not self.stopped:
			for device in self.paired_devices.keys():
				if not self.stopped:
					status = self.l2ping(device)
					old_status = self.paired_devices[device]
					new_status = old_status + status
					if new_status <= self.paired_status_maximum and new_status >= 0:
						self.paired_devices[device] = new_status
					if DEBUG:
						print device, self.paired_devices[device],  str(datetime.now())
					
				count += 1
				
				if count%100 == 0:
					self.reset_interface()
				
				if DEBUG:
					print "count:", count
					
					
	def reset_interface(self):
		if DEBUG:
			print "Reset_interface()"
		p = subprocess.Popen('sudo hciconfig hci0 reset',
							shell=True,
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT)
		p.stdout.readlines()
		sleep(self.inter_ping_delay)
			
	def get_devices_status(self):
		list = []
		for device in self.paired_devices.keys():
			d = dict()
			d['mac'] = device
			if self.paired_devices[device] > 0:
				d['status'] = 'ON'
			else:
				d['status'] = 'OFF'
			list.append(d)
		return list

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
		sleep(60*60*24*2)
		
	except:
		print "Exception"
	finally:
		d.stop()
		print "#Sttoped#\n\n"
