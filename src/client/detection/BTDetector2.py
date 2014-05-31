#!/usr/bin/python

import os
import gobject
import dbus
import dbus.mainloop.glib
from optparse import OptionParser, make_option
from threading import Thread, Lock
from datetime import datetime
from time import sleep

class BlueZ(Thread):

	DEBUG = False

	def __init__(self, hub, db=True):
		Thread.__init__(self)

		#Sudo required
		if os.geteuid() != 0:
			raise Exception("You need to have root privileges. Exiting.")
		
		self.stopped = False
		self.hub = hub
		self.db = db
		self.update_lock = Lock()
		self.last_update = datetime.now()
		self.seen_devices = list()
		self.seen_timeout = 30	# if device is not seen for x seconds it gets eliminated from the seen_devices
		self.bluetooth_memory_values = set()
		self.traking_devices = set()
		self.interface_fail = 0


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

		self.update_lock.acquire(True)
		self.update_seen_devices(device)
		self.update_lock.release()

		if device["Address"] in self.traking_devices:
			self.bluetooth_memory_values.add(addr)

	def update_seen_devices(self, device):

		time_now = datetime.now()
		new_list = list()
		new_list.append(device)

		#Appends older devices that did not timed out yet
		for seen in self.seen_devices:

			if (time_now - seen["Timestamp"]).total_seconds() < self.seen_timeout:
				if seen["Address"] != device["Address"]:
					new_list.append(seen)

		self.seen_devices = new_list

	def property_changed(self, name, value):
		if self.DEBUG:
			print name, value
		if (name == "Discovering" and not value):
			#self.mainloop.quit()
			self.scan_done = True

	def stop(self):
		if self.DEBUG:
			print "Thread Stoped"
		self.stopped = True
		self.mainloop.quit()

	def run(self):
		#Loads the settings from the DB if present
		if self.db:
			self.get_traked_devices_from_db()

		self.adapter.StartDiscovery()
		self.mainloop = gobject.MainLoop()
		self.scan_done = False
		self.mainloop.run()

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
if __name__ == '__main__':

	
	b = BlueZ(None,db=False)

	x = 0
	b.start()
	sleep(10)
	b.stop()
	#sleep(60*60*24*365)
	#try:
	#	while True:
	#		print x, "|", str(datetime.now()).split(".")[0]
	#		b.run_once()
	#		while not b.scan_done:
	#			sleep(0.25)
	#		x = x+1
	#except:
	#	print b.seen


