#!/usr/bin/env python
"""Manages programmed Actions
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.5"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from numpy import mean
from time import sleep
from random import choice
from string import ascii_uppercase, digits
from datetime import datetime
from threading import Thread

from Task import Task
from DTOs.MesurmentDTO import MesurmentDTO
from DTOs.MeasurmentEnum import DataType

class ScheduleManager(Thread):
	
	DEBUG 					= True
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
		
		
		self.tasks.append(Task(self.log_Startup, 1, one_time_task = True))			# Runs Once
		self.tasks.append(Task(self.change_Api_Key, 0, one_time_task = True))		# Runs Once

		#Append Rutines to the list
		self.tasks.append(Task(self.save_TempHumid_to_DB, 5 * 60))							# loop every  5 Min
		self.tasks.append(Task(self.save_Luminosity_to_DB, 7 * 60))							# loop every  2 Min
		self.tasks.append(Task(self.save_Current_to_DB, 1 * 60))							# loop every  1 Min
		self.tasks.append(Task(self.save_Blutooth_Presence_to_DB, 3 * 60))					# loop every  3 Min
		self.tasks.append(Task(self.save_Wifi_Presence_to_DB, 5 * 60))						# loop every  5 Min
		self.tasks.append(Task(self.update_and_Save_Exterior_Sensor_Values, 10 * 60))		# loop every 10 Min
		self.tasks.append(Task(self.change_Api_Key, 45))									# loop every 45 Sec
		#self.tasks.append(Task(self.send_BT_Presence_to_Gateway, 10))						# loop every 10 Sec
		

		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		for task in self.tasks:
			if task.can_run() and not self.stopped:
				task.run()
				#Removes the task from the execution loop
				if task.one_time_task():
					self.tasks.remove(task)

	
	def save_TempHumid_to_DB(self):
		if self.DEBUG:
			print "Scheduler: Save_TempHumid_to_DB"

		if self.hub["TEMPERATURE"] and self.hub["HUMIDITY"] and self.hub["STORAGE HANDLER"]:
			t_values = self.hub["TEMPERATURE"].dumpTemperatureMemoryValues()
			h_values = self.hub["HUMIDITY"].dumpHumidityMemoryValues()
			if len(t_values) > 0 and len(h_values) > 0:
				t_vmean = round(mean(t_values), 1)
				h_vmean = round(mean(h_values), 1)
				db = self.hub["STORAGE HANDLER"]
				db.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATUREHUMIDITY, [t_vmean, h_vmean]))
			
		else:
			print "Scheduler: Save_TempHumid_to_DB Error locating TEMPERATURE or HUMIDITY or STORAGE object"

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
			print "Scheduler: Save_Luminosity_to_DB Error locating LUMINOSITY or STORAGE object"


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
			print "Scheduler: Save_Current_to_DB Error locating CURRENT or STORAGE object"

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
			print "Scheduler: save_Blutooth_Presence_to_DB Error locating BLUETOOTH or STORAGE object"


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
			print "Scheduler: save_Wifi_Presence_to_DB Error locating WIFI or STORAGE object"



	def send_BT_Presence_to_Gateway(self):
		if self.DEBUG:
			print "Scheduler: Send_BT_Presence_to_Gateway"

		if self.hub["PUBLISHER"] and self.hub["BLUETOOTH"]:
			devices = self.hub["BLUETOOTH"].get_traked_devices()
			self.hub["PUBLISHER"].publish("Ocupants", str(len(devices)), 2)
			macs = "|"
			for device in devices:
				macs += device + "|"
			self.hub["PUBLISHER"].publish("OcupantsMAC", macs, 2)
		else:
			print "Scheduler: Send_BT_Presence_to_Gateway Error locating PUBLISHER or BLUETOOTH object"

	def update_and_Save_Exterior_Sensor_Values(self):
		if self.DEBUG:
			print "Scheduler: update_Exterior_Sensor_Values"

		if self.hub["EXTERNAL TEMPERATURE"] and self.hub["EXTERNAL HUMIDITY"] and self.hub["STORAGE HANDLER"]:
			self.hub["EXTERNAL TEMPERATURE"].updateValues()

			t_value = self.hub["EXTERNAL TEMPERATURE"].getTemperature()
			h_value = self.hub["EXTERNAL HUMIDITY"].getHumidity()
			db = self.hub["STORAGE HANDLER"]
			db.insertValue(MesurmentDTO(str(datetime.now()), DataType.EXTERIOR_TEMPERATURE_HUMIDITY, [t_value, h_value]))
			
		else:
			print "Scheduler: Save_TempHumid_to_DB Error locating EXTERNAL TEMPERATURE or EXTERNAL HUMIDITY or STORAGE object"

	def log_Startup(self):
		if self.DEBUG:
			print "Scheduler: log_Startup"

		if self.hub["STORAGE HANDLER"]:
			db = self.hub["STORAGE HANDLER"]
			db.log("System Startup")
			
		else:
			print "Scheduler: Save_TempHumid_to_DB Error locating EXTERNAL TEMPERATURE or EXTERNAL HUMIDITY or STORAGE object"
	
	def change_Api_Key(self):

		self.hub["API KEY"] = ''.join(choice(ascii_uppercase+digits) for _ in range(6))

		if self.DEBUG:
			print "Scheduler: change_Api_Key to "+self.hub["API KEY"]

#Runs only if called
if __name__ == "__main__":
	
	sm = Schedule_Manager(None)
	sm.start()
	sleep(3)
	sm.stop()
	exit(0)
