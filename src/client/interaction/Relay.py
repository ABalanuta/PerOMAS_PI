#!/usr/bin/env python
"""This Class is responsible for tigerring the Relays"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import RPi.GPIO as GPIO
from time import sleep

class Relay():
	
	DEBUG 			= True
	RELAY 			= {	"AC_SPEED_1"		:	{"Pin" : 4, "State" : False},
						"AC_SPEED_2"		:	{"Pin" : 17, "State" : False},
						"AC_SPEED_3" 		:	{"Pin" : 27, "State" : False},
						"AC_HEAT_COOL" 		:	{"Pin" : 22, "State" : False},
						"LIGHTS_X1" 		:	{"Pin" : 23, "State" : False},
						"LIGHTS_X2" 		:	{"Pin" : 24, "State" : False},}


	def __init__(self, hub):
		self.hub = hub
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(True)
		
		#Iniciates and Sets the Predefine state to each device
		for device_name in self.RELAY.keys():
			values = self.RELAY[device_name]
			GPIO.setup(values["Pin"], GPIO.OUT)
			GPIO.output(values["Pin"], values["State"])

	def set_ac_speed(self, speed):

		for relay_name, values in self.RELAY.items():

			#Turn off all ac relays responsable for speed
			if "AC_SPEED" in relay_name:
				pin = values["Pin"]
				self.RELAY[relay_name]["State"] = False
				GPIO.output(pin, False)

		#Turn on the especified speed
		if 0 <= speed <= 3:
			if speed > 0:
				relay_name = "AC_SPEED_"+str(speed)
				pin = self.RELAY[relay_name]["Pin"]
				GPIO.output(pin, True)

				if self.DEBUG:
					print "AC speed set to: "+ relay_name
			else:		
				if self.DEBUG:
					print "AC speed turned off"
	#def set_lights_x1_state(self, state):
	#	if self.DEBUG:
	#		print "Relay: set_lights_x1_state:", state

	#	pin = self.RELAY["LIGHTS_X1"]["Pin"]
	#	self.RELAY["LIGHTS_X1"]["State"] = state
	#	GPIO.output(pin, state)

	#def set_lights_x2_state(self, state):
	#	if self.DEBUG:
	#		print "Relay: set_lights_x2_state:", state

	#	pin = self.RELAY["LIGHTS_X2"]["Pin"]
	#	self.RELAY["LIGHTS_X2"]["State"] = state
	#	GPIO.output(pin, state)

	#def get_lights_x1_state(self):
	#	if self.DEBUG:
	#		print "Relay: get_lights_x1_state"

	#	return self.RELAY["LIGHTS_X1"]["State"]

	#def get_lights_x2_state(self):
	#	if self.DEBUG:
	#		print "Relay: get_lights_x2_state"

	#	return self.RELAY["LIGHTS_X2"]["State"]

	def stop(self):
		if self.DEBUG:
			print "Relay: All devices are OFF"

		GPIO.cleanup()

#Runs only if called
if __name__ == "__main__":

	try:
		r = Relay(None)
		slp = 10
		x = int(120/(4*slp))
		for y in range(0, x):
			r.set_ac_speed(0)
			sleep(slp)
			r.set_ac_speed(1)
			sleep(slp)
			r.set_ac_speed(2)
			sleep(slp)
			r.set_ac_speed(3)
			sleep(slp)
	finally:
		sleep(0.5)
		r.stop()
