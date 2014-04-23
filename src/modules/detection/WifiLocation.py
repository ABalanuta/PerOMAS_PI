#!/usr/bin/env python
"""Wifi Detection Module

Scans the APs at IST-Taguspark via SNMP and retrives the connectd MAC
addreses saving the relevant information.
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import netsnmp
import socket
import threading
from datetime import datetime
from time import sleep

#Converts the deciaml representation to hexadecimal
def get_mac(var):
	mac = var.split('.')
	mac = mac[-6:]
	for x in range(0, len(mac)):
		char = hex(int(mac[x])).split('x')[1].upper()
		if len(char) == 1:
			mac[x] = '0'+char
		else:
			mac[x] = char
	return mac[0]+':'+mac[1]+':'+mac[2]+':'+mac[3]+':'+mac[4]+':'+mac[5]
	

class ResolveDns(threading.Thread):
	
	def __init__(self, ip):
		threading.Thread.__init__(self)
		self.ip = ip
		self.dnsname = None

	def run(self):
		try:
			name, alias, addresslist = socket.gethostbyaddr(self.ip)
			self.dnsname = name.split('.')[0].upper()
		except socket.error:
			self.dnsname = None

#Retrives Reverse DNS name of an IP
def get_dns_name(ip):

	dns = ResolveDns(ip)
	dns.start()
	#timeout after .7 second
	dns.join(0.7)
	
	if dns.dnsname:
		return str(dns.dnsname)
	else:
            return None


def get_associated(ip, DEBUG=False):
	
	oid = '.1.3.6.1.4.1.9.9.273.1.2.1.1.14'
	
	dns_name = get_dns_name(ip)
	if dns_name:
		if DEBUG:
			print "Found AP "+dns_name
		
		session = netsnmp.Session( DestHost=ip, Version=2, Community='public',Timeout=10000, Retries=1, UseNumeric=1)
		session.UseLongNames = 1
		vars = netsnmp.VarList( netsnmp.Varbind(oid) )
		session.walk(vars)
		
		list = []
		for var in vars:
			mac = get_mac(var.tag+"."+var.iid)
			list.append((mac, var.val, dns_name, datetime.now()))
		return list
			
	else:
		if DEBUG:
			print "Did not Found AP"
		return []


class WifiDetector(threading.Thread):
	
	DEBUG 		= True
	IP_RANGE 	= ('172.20.3.', 1, 90)	# APs ip Range 172.20.3.1-60
	SCAN_DELAY 	= 3					# Time in seconds

	def __init__(self, hub, db=True):
		if self.DEBUG:
			print "WifiDetector.init()"
		threading.Thread.__init__(self)
		self.hub = hub
		self.db = db 		#presence of an db
		self.stopped = True
		self.detectedList = []
		self.tackList = set()
		self.presentList = []
		self.wifi_memory_values = dict()
	
	def stop(self):
		if self.DEBUG:
			print "WifiDetector.stop()"
		self.stopped = True
	
	def run(self):
		if self.DEBUG:
			print "WifiDetector.run()"
		self.stopped = False

		#Loads the settings from the DB if present
		if self.db:
			self.tackList = self.get_traked_devices_from_db()
		
		while not self.stopped:
			if len(self.tackList) > 0:
				self.update()
				for x in range(0, self.SCAN_DELAY):
					if not self.stopped:
						sleep(1)
					else:
						break
			else:
				sleep(1)
						
	def update(self):
		if self.DEBUG:
			print "WifiDetector.update()"
		
		newList = []
		for x in range(int(self.IP_RANGE[1]), int(self.IP_RANGE[2])+1):
			ip = self.IP_RANGE[0]+str(x)
			l = get_associated(ip)
			if len(l) > 0:
				newList += l
			#sleep(0.05)
		self.update_seen_list(newList)



	def update_seen_list(self, devices):
		if self.DEBUG:
			print "WifiDetector.update_seen_list()"

		for device in devices:
			if device[0] in self.tackList:
				if device[0] in self.wifi_memory_values.keys():	#if dictionary key exists
					self.wifi_memory_values[device[0]].add(device[2])	#adds the location to the set 
				else:
					self.wifi_memory_values[device[0]] = set()
					self.wifi_memory_values[device[0]].add(device[2])
				print self.wifi_memory_values

	#Dumps the cache of seen devices
	def dumpMemoryValues(self):
		b = self.wifi_memory_values
		self.wifi_memory_values = dict()

		#Transfoms the set of locations into a String
		for key in b.keys():
			string = "|"
			for location in b[key]:
				string = string + location + "|"
			b[key] = string

		return b

	def get_traked_devices_from_db(self):
		while "STORAGE HANDLER" not in self.hub.keys():
			sleep(0.5)

		devices = self.hub["STORAGE HANDLER"].readSettings("Wifi_Tracking_Devices")
		return devices
	
	def track_device(self, newMac):
		if self.DEBUG:
			print "WifiDetector.track_device()", newMac

		if newMac not in self.tackList:
			self.tackList.add(newMac)

			if self. db:
				while "STORAGE HANDLER" not in self.hub.keys():
					sleep(0.2)

				self.hub["STORAGE HANDLER"].writeSettings("Wifi_Tracking_Devices", 
														self.tackList)
	

##Executed if only is the main app		
if __name__ == '__main__':
	
	wd = WifiDetector(None,db=False)
	wd.track_device('40:B0:FA:C7:A1:EB')
	
	try:
		wd.start()
		sleep(3600)
		wd.stop()
	except KeyboardInterrupt:
		wd.stop()
	
		
		
		
		
