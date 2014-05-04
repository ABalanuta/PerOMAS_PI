#!/usr/bin/env python
"""This Class is responsible for tigerring the Relays"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import RPi.GPIO as GPIO
from time import sleep

class Relay():
	
	DEBUG 			= False

	RELAY_1_PINS	= [4, 17, 27, 22]	# GPIO.BCM Pin for the four chanels of the Relay
	RELAY_2_PINS	= [23, 24, 25, 18]	#

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

	r = Relay(None)
	pin = r.RELAY["AC_SPEED_1"]["Pin"]
	GPIO.output(pin, True)
	sleep(5)
	#sleep(1)
	r.stop()
