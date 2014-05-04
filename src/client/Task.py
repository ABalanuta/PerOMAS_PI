#!/usr/bin/env python
""" Defines a task """
__author__ = "Artur Balanuta"
__version__ = "1.0.3"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from datetime import datetime

class Task():
	
	LAST_EXECUTED 	= None	# Timestamp of when the Task where executed
	SLEEP 			= 60	# Time in seconds before the task is need to be run again
	ACTION 			= None	# Pointer to the function to be executed
	ONE_TIME_TASK	= False # Routine task or not (Routine by default)
	
	def __init__(self, action, sleep, one_time_task = False, var = None):
		self.ONE_TIME_TASK = one_time_task
		self.LAST_EXECUTED = datetime.now()
		self.SLEEP = sleep
		self.ACTION = action
		self.var = var
		
	def run(self):

		if self.var != None:
			self.ACTION(self.var)
		else:	
			self.ACTION()
		
		self.LAST_EXECUTED = datetime.now()
	
	def can_run(self):
		if (datetime.now() - self.LAST_EXECUTED).seconds >= self.SLEEP:
			return True
		else:
			return False

	def one_time_task(self):
		return self.ONE_TIME_TASK
	
	def get_variables(self):
		return self.var

#Runs only if called
if __name__ == "__main__":
	
	def ole():
		print "Hello World"
	def one_time():
		print "One Time"
	
	def my_variables(var):
		print "Vars:"+str(var)

	a = Task(ole, 1)
	b = Task(my_variables, 3, var=[1, 2, "ole"])

	while True:
		if a.can_run():
			a.run()

		if b.can_run():
			b.run()	
	
	
	
	

