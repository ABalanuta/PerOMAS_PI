#!/usr/bin/env python
""" Uses the colective data of the sensors, actuators and comunication
devices to maintain a confortable Office for the occupants"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from threading import Thread
from time import sleep

class Logic_Engine(Thread):

	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 0.5	#sleeps X seconds befor cheking the need of executing any task

	def __init__(self, hub):
		Thread.__init__(self)

	def stop(self):
		self.stopped = True
	
	def run(self):
		self.stopped = False

		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		print "Update"

#Runs only if called
if __name__ == "__main__":
	

	lm = Logic_Engine(None)
	lm.start()
	sleep(3)
	lm.stop()