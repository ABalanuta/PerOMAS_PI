#!/usr/bin/env python
"""Temperature and Humidity Module
for reading the values from the HTU21D sensor"""

__author__ = "Artur Balanuta"
__version__ = "1.0.3"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from time import sleep
from threading import Thread
from datetime import datetime

from Python2.sht21 import SHT21



class TempHumid(Thread):

	def __init__(self, hub):
		Thread.__init__(self)
		self.stopped = False
		self.hub = hub
		self.executable = SHT21(device_number=1)
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.temp = 0
		self.humid = 0
		self.update_interval = 2 # 2 sec
		self.temperature_memory_values = []
		self.humidity_memory_values = []
		#Runs after var declaration
		self.update()# Runs one time
		
	def stop(self):
		self.stopped = True
		self.executable.close()

	def run(self):
		while not self.stopped:
			self.update()
			sleep(self.update_interval)


	def update(self):

		while not self.stopped:

			try:
				t = self.executable.read_temperature() - 1.9
				h = self.executable.read_humidity()  + 4
			except:
				print str(datetime.now()), "HTU21D sensor Read Error"
				sleep(0.05)
				continue
			
			self.temp = t
			self.temperature_memory_values.append(self.temp)

			self.humid = h
			self.humidity_memory_values.append(self.humid)
			self.last_update = datetime.now()
			break


	#Dumps the cache of temperature values
	def dumpTemperatureMemoryValues(self):
		t = self.temperature_memory_values
		self.temperature_memory_values = []
		return t
	#Dumps the cache of humidity values
	def dumpHumidityMemoryValues(self):
		h = self.humidity_memory_values
		self.humidity_memory_values = []
		return h
		
	def getTemperature(self):
		return self.temp

	def getHumidity(self):
		return self.humid

	def getLastUpdate(self):
		return str(self.last_update).split(".")[0].split()[1]

#Runs only if called
if __name__ == "__main__":

	started = datetime.now()

	print "#TEST#"
	print "#Starting#"
	d = TempHumid(None)
	d.start()
	try:
		while True:
			print "\tTemp:", d.temp, "\tHumid:", d.humid
			sleep(4)
	except KeyboardInterrupt: 
		d.stop()

	print "#Sttoped#\n\n"
