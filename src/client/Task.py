#!/usr/bin/env python
""" Defines a task """
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from datetime import datetime

class Task():
	
	LAST_EXECUTED 	= None	# Timestamp of when the Task where executed
	SLEEP 			= 60	# Time in seconds before the task is need to be run again
	ACTION 			= None	# Pointer to the function to be executed
	
	def __init__(self, action, sleep):
		self.LAST_EXECUTED = datetime.now()
		self.SLEEP = sleep
		self.ACTION = action
		
	def run(self):
		self.ACTION()
		self.LAST_EXECUTED = datetime.now()
	
	def can_run(self):
		if (datetime.now() - self.LAST_EXECUTED).seconds > self.SLEEP:
			return True
		else:
			return False
	
#Runs only if called
if __name__ == "__main__":
	
	def ole():
		print "Hello World"
	
	a = Task(ole, 2)
	while True:
		if a.can_run():
			a.run()	
	
	
	
	

