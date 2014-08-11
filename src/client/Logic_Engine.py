#!/usr/bin/env python
""" Uses the colective data of the sensors, actuators and comunication
devices to maintain a confortable Office for the occupants"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from threading import Thread
from time import sleep, localtime, time

class Logic_Engine(Thread):

	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 1 		#sleeps X seconds befor cheking the need of executing any task
	MARGIN 					= 0.35
	AC_TARGET 		 		= 24
	AC_MODE_AUTO 			= False

	def __init__(self, hub):
		Thread.__init__(self)
		self.hub = hub
		
	def stop(self):
		self.stopped = True
	
	def run(self):
		self.stopped = False

		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)
			
	def update(self):
		if self.DEBUG:
			print "Update"

		self.checkUserRules()

		if self.AC_MODE_AUTO:
			self.checkTermostatLogic()

	def checkUserRules(self):

		users = None

		if "USER MANAGER" in self.hub.keys():
			users = self.hub["USER MANAGER"].users
		else:
			if self.DEBUG:
				print "Could not find users"
			return

		for username, user in users.items():
			for rule in user.rules:
				t = rule.try_execute()
				if self.DEBUG:
					print "checkUserRules: Rule: "+rule.alias, t

	def checkTermostatLogic(self):
		
		if self.hub["TEMPERATURE"] and self.hub["RELAY"]:

			curr_temp = self.hub["TEMPERATURE"].getTemperature()
			relay = self.hub["RELAY"]

			#Shuts Down the AC if out of Working Hours
			if not self.isWorkingHours():
				relay.set_ac_speed(0)
				return

			#Turn ON Fan if too Hot
			if curr_temp > self.AC_TARGET+(self.MARGIN*3):
				relay.set_ac_speed(3)

			elif curr_temp > self.AC_TARGET+self.MARGIN:
				relay.set_ac_speed(2)

			elif curr_temp > self.AC_TARGET:
				relay.set_ac_speed(2)

			#Turn OFF FAN if temp Perfect
			elif curr_temp < self.AC_TARGET-self.MARGIN:
				relay.set_ac_speed(0)

		else:
			print "Error, no TEMPERATURE Sensor or Relay Object"

	def isWorkingHours(self):
		current_hour = localtime(time()).tm_hour
		if current_hour > 20 or current_hour < 8:
			return False
		else:
			return True

	def getACMode(self):
		if self.AC_MODE_AUTO:
			return "Auto"
		else:
			return "Manual"

	def setACMode(self, mode):
		if mode == "Auto":
			self.AC_MODE_AUTO = True
		elif mode == "Manual":
			self.AC_MODE_AUTO = False

	def set_AC_Setpoint(self, setpoint):
		self.AC_TARGET = float(setpoint)
		if self.DEBUG:
			print "New AC setpoint", self.AC_TARGET

	def get_AC_Setpoint(self):
		return self.AC_TARGET

#Runs only if called
if __name__ == "__main__":
	

	lm = Logic_Engine(None)
	lm.start()
	sleep(3)
	lm.stop()