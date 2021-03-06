#!/usr/bin/env python
"""Gateway Application Main Class

Starts the different modules composing the Application
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import time, signal, sys
from time import sleep
from datetime import datetime
from communication.Pub_Sub import MQTTC

#from Scheduler_Manager import ScheduleManager
#from Storage_Handler import StorageHandler




##Executed if only is the main app		
if __name__ == '__main__':	
	

	DEBUG		= True		# Debug Mode
	
	def signal_handler(signal, frame):
		
		print 'You pressed Ctrl+C!'

		for key, value in hub.items():
			if "STORAGE HANDLER" is not key:
				if DEBUG:
					print "Stopping", key
				if value.stop:
					value.stop()
		
		#Storage stops Last
		if "STORAGE HANDLER" in hub.keys():
			if DEBUG:
				print "Stopping STORAGE HANDLER"
			hub["STORAGE HANDLER"].stop()
		
		sys.exit(0)
	
	#Register Signal
	signal.signal(signal.SIGINT, signal_handler)
	#print 'Press Ctrl+C to exit'
	
	
	if DEBUG:
		print "-> Starting Gateway <-"
	
	try:
		
		#Main object used for sharing
		hub = dict()

		#Starts the Storage Handler
		#sh = StorageHandler(hub)
		#hub["STORAGE HANDLER"] = sh
		#if DEBUG:
		#	print "Storage is ON"
	
		
		
		#Starts the Scheduler Manager
		#sm = ScheduleManager(hub)
		#sm.start()
		#hub["SCHEDULE MANAGER"] = sm
		#if DEBUG:
		#	print "Scheduler Manager started automation"
		
		#Starts The MQTT Listener
		mqtt = MQTTC(hub, gateway=True)
		mqtt.start()
		hub["SUBSCRIBER"] = mqtt
		if DEBUG:
			print "Subscriber is ON"



		while True:
			sleep(4)
			
	except:
		raise





