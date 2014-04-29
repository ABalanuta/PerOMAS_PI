#!/usr/bin/env python
"""Manages programmed Actions
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from numpy import mean
from time import sleep
from datetime import datetime
from threading import Thread

from Task import Task

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
		
		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		for task in self.tasks:
			if task.can_run() and not self.stopped:
				task.run()

				
#Runs only if called
if __name__ == "__main__":
	
	sm = Schedule_Manager(None)
	sm.start()
	sleep(3)
	sm.stop()
	exit(0)

	
	
	
	
	
	

