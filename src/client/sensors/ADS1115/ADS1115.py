#!/usr/bin/env python
"""Consumption Estimation

Uses the ADS1x15 Adafruit lib to read values from the first
channel of the ADC and converts to Real power consumption in Watts.
"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from time import sleep
from threading import Thread
from datetime import datetime
from numpy import mean
from Adafruit_ADS1x15 import ADS1x15



class ADS1115(Thread):

	UPDATE_INTERVAL 	= 0 	# time in seconds
	ADS1115 			= 0x01	# 16-bit ADC
	CHANNEL 			= 0 	# ADC Channel (from 0 to 3)
	PGA					= 2048	# programable gain, possible values (256,512,1024,2048,4096,6144)
	SAMPLES 			= 860 	# Samples per Second, possible values (8,16,32,128,256,475,860)
	CALIBRATION_FACTOR 	= 2.4 	# Used to ajust the read values to the real consumption values
	BASE_CONSUMPTION	= 1.14 	# Base consumption of the sensor
	FILTER_MINIMUM		= 0.2 	# Values lower that this are considered noise and are filtered as Zero
	MESURMENTS			= 60	# Number of mesurments per second (Hz)


	def __init__(self, hub):
		Thread.__init__(self)
		self.hub = hub
		self.started = datetime.now()
		self.last_update = datetime.now()
		self.watts = 0.0
		self.watts_memory_values = []
		self.sensor = ADS1x15(ic=self.ADS1115)
		self.sensor.startContinuousConversion(self.CHANNEL, self.PGA, self.SAMPLES) #reads values +-1V with 860 samples/s
		self.stopped = False
		#Runs after var declaration
		self.update()# Runs one time


	def stop(self):
		self.stopped = True
		sleep(1.1)
		self.sensor.stopContinuousConversion()

	def run(self):
		self.stopped = False
		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.UPDATE_INTERVAL)

	def update(self):

		values = []
		for x in range(0, self.MESURMENTS):
			values.append(self.sensor.getLastConversionResults())
			sleep(1.0/self.MESURMENTS)
		w = mean(values) * self.CALIBRATION_FACTOR - self.BASE_CONSUMPTION
		
		#Filte very small walues
		if w > self.FILTER_MINIMUM:
			self.watts = w
		else:
			self.watts = 0

		self.watts_memory_values.append(self.watts)
		#self.last_update = datetime.now()
			
	def runtime(self):
		return str(self.last_update-self.started).split(".")[0]

	#Retrurns the last read value
	def getValue(self):
		return self.watts

	#Dumps the cache of luminosity values
	def dumpMemoryValues(self):
		w = self.watts_memory_values
		self.watts_memory_values = []
		return w
		
#Runs only if called
if __name__ == "__main__":
	
	print "#TEST#"
	print "#Starting#"
	l = ADS1115(None)
	l.start()
	sleep(1)
	try:
		while True:
			print l.watts
			sleep(1)
	except: 
		l.stop()
	print "#Sttoped#\n\n"
