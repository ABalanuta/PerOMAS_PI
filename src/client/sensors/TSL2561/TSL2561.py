#!/usr/bin/env python
"""Luminosity Module for reading the values from the TSL2561 sensor"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

#!/usr/bin/env python
"""Temperature and Humidity Module
for reading the values from the HTU21D sensor"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from time import sleep
from threading import Thread
from datetime import datetime
from TSL2561_Driver import Adafruit_TSL2651



class TSL2561(Thread):

	UPDATE_INTERVAL = 1 # time in seconds

	def __init__(self, hub):
		Thread.__init__(self)
		self.hub = hub
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.lux = 0
		self.luminosity_memory_values = []
		self.sensor = Adafruit_TSL2651()
		self.sensor.enableAutoGain(True)

		#Runs after var declaration
		self.update()# Runs one time


	def stop(self):
		self.stopped = True

	def run(self):
		self.stopped = False
		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.UPDATE_INTERVAL)

	def update(self):
		value = self.sensor.calculateLux()
		self.lux = int(value)
		self.luminosity_memory_values.append(value)
		self.last_update = datetime.now()
			
	def runtime(self):
		return str(self.last_update-self.started).split(".")[0]

	#Retrurns the last read value
	def getValue(self):
		return self.lux

	#Dumps the cache of luminosity values
	def dumpMemoryValues(self):
		t = self.luminosity_memory_values
		self.luminosity_memory_values = []
		return t
		
#Runs only if called
if __name__ == "__main__":
	
	print "#TEST#"
	print "#Starting#"
	l = TSL2561(None)
	l.start()
	try:
		while True:
			print l.lux
			print l.luminosity_memory_values
			sleep(1)
	except: 
		l.stop()
	
	print "#Sttoped#\n\n"
