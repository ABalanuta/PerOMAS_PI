#!/usr/bin/env python
"""Manages programmed Actions
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import numpy as np

from time import sleep
from datetime import datetime
from threading import Thread

from Task import Task
from DTOs.MesurmentDTO import MesurmentDTO
from DTOs.MeasurmentEnum import DataType

class ScheduleManager(Thread):
	
	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 1	#sleeps X seconds befor cheking the need of executing any task
	
	def __init__(self, hub):
		Thread.__init__(self)
		
		self.hub = hub
		self.stopped = True
		self.tasks = []
		
		
	def stop(self):
		self.stopped = True
	
	def run(self):
		self.stopped = False
		
		#Append Rutines to the list
		self.tasks.append(Task(self.save_Temperature_to_DB, 5*60)) # loop every 5 Mins
		self.tasks.append(Task(self.save_Humidity_to_DB, 5*60))	# loop every 5 Min
		
		while not self.stopped:
			self.update()
			sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		if self.DEBUG:
			print "Update"
		for task in self.tasks:
			if task.can_run() and not self.stopped:
				task.run()

	
	def save_Temperature_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Temperature_to_DB"
		if self.hub["TEMPERATURE"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["TEMPERATURE"].dumpTemperatureMemoryValues()
			mean = np.mean(values)
			db = self.hub["STORAGE HANDLER"]
			db.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, mean))
			
		else:
			print "Scheduler: Save_Temperature_to_DB locating TEMPERATURE or STORAGE object"
	
	def save_Humidity_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Humidity_to_DB"
		if self.hub["HUMIDITY"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["HUMIDITY"].dumpHumidityMemoryValues()
			mean = np.mean(values)
			db = self.hub["STORAGE HANDLER"]
			db.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, mean))
		else:
			print "Scheduler: Save_Temperature_to_DB locating HUMIDITY or STORAGE object"
		
#Runs only if called
if __name__ == "__main__":
	
	sm = Schedule_Manager(None)
	sm.start()
	sleep(3)
	sm.stop()
	exit(0)

	
	
	
	
	
	

