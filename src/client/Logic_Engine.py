#!/usr/bin/env python
""" Uses the colective data of the sensors, actuators and comunication
devices to maintain a confortable Office for the occupants"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from threading import Thread
from time import sleep, localtime, time

class Logic_Engine(Thread):

	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 20 		#sleeps X seconds befor cheking the need of executing any task
	MARGIN 					= 0.33
	AC_TARGET 		 		= 24.5
	AC_MODE_AUTO 			= True

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

			# if out of working ours and Automatic
			# turn off he AC
			if not self.isWorkingHours():
				if "RELAY" in self.hub.keys():
					self.hub["RELAY"].set_ac_speed(0)

			#continue with the normal scheduler
			else:
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

		if self.hub["TEMPERATURE"] and "RELAY" in self.hub.keys():

			curr_temp = self.hub["TEMPERATURE"].getTemperature()
			relay = self.hub["RELAY"]

			#present_users = self.hub["USER MANAGER"].getPresentUsers()

			#if len(present_users) > 0:
			if True:
				##Calculates the average temperature of the users in the office
				#target_setpoint = 0
				target_setpoint = self.AC_TARGET
				#for user in present_users:
				#	target_setpoint += self.hub["USER MANAGER"].getUser(user).setpoint
				#target_setpoint /= len(present_users)

				#Shuts Down the AC if out of Working Hours or no Users in the Office
				#if not self.isWorkingHours():
				#	relay.set_ac_speed(0)
				#	return


				#Ajusts AC Mode
				if target_setpoint > curr_temp:
					relay.set_ac_mode("Heat")
				else:
					relay.set_ac_mode("Cool")

				#Ajusts the fan speed
				if abs(curr_temp - target_setpoint) > self.MARGIN*2.5:
					relay.set_ac_speed(3)

				#elif abs(curr_temp - target_setpoint) > self.MARGIN*2:
				#	relay.set_ac_speed(2)

				elif abs(curr_temp - target_setpoint) > self.MARGIN*1.25:
					relay.set_ac_speed(1)

				#Turn OFF FAN if temp Perfect
				else:
					relay.set_ac_speed(0)

			else:
				#Shuts Down the AC if nobody is in the office
				relay.set_ac_speed(0)
		else:
			sleep(0.2)


	def isWorkingHours(self):
		current_hour = localtime(time()).tm_hour
		if current_hour > 21 or current_hour < 8:
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
