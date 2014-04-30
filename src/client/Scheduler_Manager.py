#!/usr/bin/env python
"""Manages programmed Actions
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.4"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from numpy import mean
from time import sleep
from datetime import datetime
from threading import Thread

from Task import Task
from DTOs.MesurmentDTO import MesurmentDTO
from DTOs.MeasurmentEnum import DataType

class ScheduleManager(Thread):
	
	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 1	#sleeps X seconds befor cheking the need of executing any task
	MINUTE					= 60

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

		self.tasks.append(Task(self.save_Temperature_to_DB, 5*self.MINUTE)) 		# loop every 5 Mins
		self.tasks.append(Task(self.save_Humidity_to_DB, 5*self.MINUTE))			# loop every 5 Min
		self.tasks.append(Task(self.save_Luminosity_to_DB, 2*self.MINUTE))			# loop every 2 Min
		self.tasks.append(Task(self.save_Current_to_DB, 1*self.MINUTE))				# loop every 1 Min
		self.tasks.append(Task(self.save_Blutooth_Presence_to_DB, 3*self.MINUTE))	# loop every 3 Min
		self.tasks.append(Task(self.save_Wifi_Presence_to_DB, 5*self.MINUTE))		# loop every 5 Min
		self.tasks.append(Task(self.send_BT_Presence_to_Gateway, 2))				# loop every 1/2 Min

		
		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		for task in self.tasks:
			if task.can_run() and not self.stopped:
				task.run()

	
	def save_Temperature_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Temperature_to_DB"

		if self.hub["TEMPERATURE"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["TEMPERATURE"].dumpTemperatureMemoryValues()
			if len(values) > 0:
				vmean = round(mean(values), 1)
				db = self.hub["STORAGE HANDLER"]
				db.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, [vmean]))
			
		else:
			print "Scheduler: Save_Temperature_to_DB locating TEMPERATURE or STORAGE object"
	
	def save_Humidity_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Humidity_to_DB"

		if self.hub["HUMIDITY"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["HUMIDITY"].dumpHumidityMemoryValues()
			if len(values) > 0:
				vmean = round(mean(values), 1)
				db = self.hub["STORAGE HANDLER"]
				db.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, [vmean]))
		else:
			print "Scheduler: Save_Humidity_to_DB locating HUMIDITY or STORAGE object"

	def save_Luminosity_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Luminosity_to_DB"

		if self.hub["LUMINOSITY"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["LUMINOSITY"].dumpMemoryValues()
			if len(values) > 0:
				vmean = round(mean(values), 1)
				db = self.hub["STORAGE HANDLER"]
				db.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, [vmean]))
		else:
			print "Scheduler: Save_Luminosity_to_DB locating LUMINOSITY or STORAGE object"


	def	save_Current_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Current_to_DB"

		if self.hub["CURRENT"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["CURRENT"].dumpMemoryValues()
			if len(values) > 0:
				vmean = round(mean(values), 1)
				db = self.hub["STORAGE HANDLER"]
				db.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, [vmean]))
		else:
			print "Scheduler: Save_Current_to_DB locating CURRENT or STORAGE object"

	def	save_Blutooth_Presence_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Blutooth_Presence_to_DB"

		if self.hub["BLUETOOTH"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["BLUETOOTH"].dumpMemoryValues()
			if len(values) > 0:
				db = self.hub["STORAGE HANDLER"]
				date = str(datetime.now())
				for device in values:
					db.insertValue(MesurmentDTO(date, DataType.BT_PRESENCE, [device]))
		else:
			print "Scheduler: save_Blutooth_Presence_to_DB locating BLUETOOTH or STORAGE object"


	def	save_Wifi_Presence_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_Wifi_Presence_to_DB"

		if self.hub["WIFI"] and self.hub["STORAGE HANDLER"]:
			values = self.hub["WIFI"].dumpMemoryValues()
			if len(values) > 0:
				db = self.hub["STORAGE HANDLER"]
				date = str(datetime.now())
				for device in values.keys():
					db.insertValue(MesurmentDTO(date, DataType.WIFI_PRESENCE, [device, values[device]]))
		else:
			print "Scheduler: save_Wifi_Presence_to_DB locating WIFI or STORAGE object"



	def send_BT_Presence_to_Gateway(self):
		if self.DEBUG:
			print "Scheduler: Send_BT_Presence_to_Gateway"

		if self.hub["PUBLISHER"] and self.hub["BLUETOOTH"]:
			devices = self.hub["BLUETOOTH"].get_traked_devices()
			self.hub["PUBLISHER"].publish("Ocupants", str(len(devices)), 2)
			self.hub["PUBLISHER"].publish("OcupantsMAC", str(devices), 2)
		else:
			print "Scheduler: Send_BT_Presence_to_Gateway locating PUBLISHER or BLUETOOTH object"

#Runs only if called
if __name__ == "__main__":
	
	sm = Schedule_Manager(None)
	sm.start()
	sleep(3)
	sm.stop()
	exit(0)

	
	
	
	
	
	

