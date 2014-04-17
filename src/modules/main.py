#!/usr/bin/env python
"""Application Main Class

Starts the different modules composing the Application
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import time, signal, sys
from time import sleep
from datetime import datetime
from sensors.HTU21D.HTU21D import TempHumid
#from sensors.wifi_detect.WifiLocation import WifiDetector
from detection.BTDetector import BTDetector
from interaction.lcd.LCDmenu import LCD
#from web.web import WebManager
from Scheduler_Manager import Schedule_Manager





##Executed if only is the main app		
if __name__ == '__main__':	
	

	DEBUG 			= True		# Debug Mode
	CLI_INTERFACE	= False		# 
	WEB_INTERFACE	= False		# 
	
	def signal_handler(signal, frame):
		
		print 'You pressed Ctrl+C!'
		for key, value in hub.items():
			if DEBUG:
				print "Stopping", key
			if value.stop:
				value.stop()
				
		sys.exit(0)
	
	signal.signal(signal.SIGINT, signal_handler)
	#print 'Press Ctrl+C to exit'
	
	
	
	if DEBUG:
		print "-> Starting main <-"
	
	try:
		
		#Main object used for sharing
		hub = dict()
	
		#Start Temperature/Humidity Sensor
		th = TempHumid(hub)
		th.start()
		hub["TEMPERATURE"] = th
		hub["HUMIDITY"] = th
		if DEBUG:
			print "T/H sensor ON"
			
		#Starts Wifi Detector
		#wifi = WifiDetector(hub)
		#wifi.start()
		#hub["WIFI"] = wifi
		#wifi.track('40:B0:FA:C7:A1:EB')
		#if DEBUG:
		#	print "WIFI sensor ON"
		
		#Starts BT Detector
		#bt = BTDetector(hub)
		#bt.start()
		#hub["BLUETOOTH"] = bt
		#if DEBUG:
		#	print "BT sensor ON"
		
		#Starts LCD
		#lcd = LCD(hub)
		#lcd.start()
		#hub["LCD"] = lcd
		#if DEBUG:
		#	print "LCD sensor ON"
		
		#Starts the Scheduler Manager
		sm = Schedule_Manager(hub)
		sm.start()
		hub["SCHEDULE MANAGER"] = sm
		if DEBUG:
			print "Scheduler Manager started automation"
		
		
		
		#Starts Web Server
		#Must be last (Blocking)
		if WEB_INTERFACE:
			wm = WebManager(hub)
			wm.start()
		
		while True:
			sleep(4)
			
			# TEmp and Humid
			#print "\n#Temp and Humidity"
			#print "\t", hub.temp_humid.temp, "C ", hub.temp_humid.humid, "% Last Update:", hub.temp_humid.last_update
			
			# Detected BT devices
			#print "#Last seen BT devices"
			#for device in hub.bt.seen_devices:
			#	print "\t", device["Name"], "seen ", (datetime.now() - device["Last seen"]).total_seconds(), "seconds ago !"
			#print "\n"
			
	except:
		raise





