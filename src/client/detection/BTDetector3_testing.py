#!/usr/bin/env python
"""Bluetooth Detection Module

Detects bluetooth beacons sent from devices and stores for a short period,
Invokes CLI commands and bluez python code.
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import signal
import subprocess
import gobject
import dbus
import dbus.mainloop.glib
from optparse import OptionParser, make_option
from time import sleep
from threading import Thread
from datetime import datetime

#Debugging Mode
DEBUG = True

class BTExecutor(Thread):
	
	DEBUG = True
	VALUE = None #Return value
	TEMP  = list()
	
	def __init__(self):
		Thread.__init__(self)


		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

		bus = dbus.SystemBus()
		manager = dbus.Interface(bus.get_object("org.bluez", "/"),
								"org.bluez.Manager")

		option_list = [
				make_option("-i", "--device", action="store",
						type="string", dest="dev_id"),
				]
		parser = OptionParser(option_list=option_list)

		(options, args) = parser.parse_args()

		if options.dev_id:
			adapter_path = manager.FindAdapter(options.dev_id)
		else:
			adapter_path = manager.DefaultAdapter()

		self.adapter = dbus.Interface(bus.get_object("org.bluez", adapter_path),
								"org.bluez.Adapter")

		bus.add_signal_receiver(self.device_found,
				dbus_interface = "org.bluez.Adapter",
						signal_name = "DeviceFound")

		bus.add_signal_receiver(self.property_changed,
				dbus_interface = "org.bluez.Adapter",
						signal_name = "PropertyChanged")



	def device_found(self, address, properties):

		self.last_update = datetime.now()
		device = dict()
		device["Timestamp"] = datetime.now()
		device["Name"] = ""
		device["Address"] = address.encode('ascii','ignore')

		if properties["Name"]:
			device["Name"] = properties["Name"].encode('ascii','ignore')

		if self.DEBUG:
			print  str(datetime.now()).split(".")[0], "Found", device["Address"], device["Name"]

		#ignores Duplicates
		for dev in self.TEMP:
			if dev["Address"] == device["Address"]:
				return

		self.TEMP.append(device)

		if self.DEBUG:
			print  str(datetime.now()).split(".")[0], "Found", device["Address"], device["Name"]



	def property_changed(self, name, value):
		if self.DEBUG:
			print name, value, str(datetime.now()).split(".")[0]
		if (name == "Discovering" and not value):
			self.mainloop.quit()

	def run(self):

		self.adapter.StartDiscovery()
		self.mainloop = gobject.MainLoop()


		if self.DEBUG:
			print "1", str(datetime.now()).split(".")[0]

		self.mainloop.run()

		if self.DEBUG:
			print "2", str(datetime.now()).split(".")[0]

		# make it the returning values
		self.VALUE = self.TEMP

	def stop(self):
		self.mainloop.quit()


class BTDetector(Thread):

	def __init__(self, hub, db=True):
		Thread.__init__(self)
		
		#Sudo required
		if os.geteuid() != 0:
			raise Exception("You need to have root privileges. Exiting.")
			
		self.stopped = False
		self.hub = hub
		self.db = db
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.seen_devices = list()
		self.seen_timeout = 30	# if device is not seen for x seconds it gets eliminated from the seen_devices
		self.bluetooth_memory_values = set()
		self.traking_devices = set()
		self.interface_fail = 0
		self.running_exe = None


	def stop(self):
		self.stopped = True
		if self.running_exe:
			self.running_exe.stop()

		
		
	def runtime(self):
		return str(self.last_update-self.started).split(".")[0]
	
	def run(self):

		#Resets the BT interface befor starting the Search
		self.reset_interface()
		
		#Loads the settings from the DB if present
		if self.db:
			self.get_traked_devices_from_db()

		while not self.stopped:
			
			if DEBUG:
				print "\n-----------------------------------"
			sleep(0.5)
			exe = BTExecutor()
			exe.start()
			self.running_exe = exe
			exe.join(16) #Wait 16 seconds for the scan to be preformed

			if self.stopped:
				break
			print "exe.value", exe.value
			if isinstance(exe.value, list):

				self.last_update = datetime.now()
				self.update_seen_list(exe.value)

				for device in exe.value:
					addr = device["Address"]
					if addr in self.traking_devices:
						self.bluetooth_memory_values.add(addr)

				if DEBUG:
					print "Found: " 
					for f in exe.value:
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
		
		
		#Appends older devices that did not timed out yet
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
		while not self.stopped:
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

	#Dumps the cache of seen devices
	def dumpMemoryValues(self):
		b = self.bluetooth_memory_values
		self.bluetooth_memory_values = set()
		return b

	def get_traked_devices_from_db(self):
		while "STORAGE HANDLER" not in self.hub.keys():
			sleep(0.5)

		devices = self.hub["STORAGE HANDLER"].readSettings("Bluetooth_Tracking_Devices")
		if devices:
			self.traking_devices = devices

	def track_device(self, MAC):
		if MAC not in self.traking_devices:
			self.traking_devices.add(MAC)

			if self.db:
				while "STORAGE HANDLER" not in self.hub.keys():
					sleep(0.2)

				self.hub["STORAGE HANDLER"].writeSettings("Bluetooth_Tracking_Devices", 
														self.traking_devices)

	def kill_mod(self):
		subprocess.Popen('sudo rmmod btusb', shell=True)
		sleep(1)
		subprocess.Popen('sudo modprobe btusb', shell=True)
		sleep(1)

	#returns a list of devices seen in the last self.seen_timeout seconds
	def get_discovered_devices(self):		
		return self.seen_devices
	
	#returns a list of tracked devices that where observed lastly
	def get_traked_devices(self):
		
		ret = []
		for device in self.seen_devices:
			addr = device["Address"]
			if addr in self.traking_devices:
				ret.append(addr)
		return ret

					
#Runs only if called
if __name__ == "__main__":


	b1 = BTExecutor()
	b1.start()
	while not b1.VALUE:
		sleep(0.1)
	print "DONE", '\n'
	b1 = None

	b2 = BTExecutor()
	b2.start()
	while not b2.VALUE:
		sleep(0.1)
	print "DONE", '\n'
	b2 = None

	b3 = BTExecutor()
	b3.start()
	while not b3.VALUE:
		sleep(0.1)
	print "DONE", '\n'
	b3 = None








	#started = datetime.now()
	# d = BTDetector(None,db=False)
	# try:
	# 	print "#TEST#"
	# 	print "#Starting#"
	# 	d.start()
	# 	sleep(60*60*24*356)
		
	# except:
	# 	print "Exception"
	
	# finally:
	# 	d.stop()
	# 	print "#Sttoped#\n\n"
	# 	print "-----------------"
	# 	for x in d.seen_devices:
	# 		print x
	# 	print "-----------------"
