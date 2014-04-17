#!/usr/bin/env python
"""Manages programmed Actions
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from time import sleep
from threading import Thread

from Task import Task

class Schedule_Manager(Thread):
	
	DEBUG 					= True
	SLEEP_BETWEEN_CHECKS 	= 2	#sleeps X seconds befor cheking the need of executing any task
	
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
		self.tasks.append(Task(self.save_Temperature_to_DB, 5*1))
		self.tasks.append(Task(self.save_Humidity_to_DB, 5*1))
		
		while not self.stopped:
			self.update()
			
	def update(self):
		if self.DEBUG:
			print "Update"
		for task in self.tasks:
			if task.can_run():
				task.run()
		sleep(self.SLEEP_BETWEEN_CHECKS)
			

	
	def save_Temperature_to_DB(self):
		print "task save_Temperature_to_DB"
	
	def save_Humidity_to_DB(self):
		print "task save_Humidity_to_DB"
		
		
#Runs only if called
if __name__ == "__main__":
	
	sm = Schedule_Manager(None)
	sm.start()
	sleep(3)
	sm.stop()
	exit(0)

	
	
	
	
	
	

