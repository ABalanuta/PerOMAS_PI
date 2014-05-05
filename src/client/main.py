#!/usr/bin/env python
"""Application Main Class

Starts the different modules composing the Application
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import time, signal, sys
from time import sleep
from datetime import datetime
from sensors.HTU21D.HTU21D import TempHumid #Temp/Humid
from sensors.TSL2561.TSL2561 import TSL2561	#Lux
from sensors.ADS1115.ADS1115 import ADS1115	#Current
from detection.WifiLocation import WifiDetector
from detection.BTDetector import BTDetector
from interaction.lcd.LCDmenu import LCD
from interaction.Relay import Relay
from communication.Pub_Sub import MQTTC
from web.web import *
from Scheduler_Manager import ScheduleManager
from Storage_Handler import StorageHandler




##Executed if only is the main app		
if __name__ == '__main__':	
	

	DEBUG		= True		# Debug Mode
	CLI_INTERFACE	= False		# 
	WEB_INTERFACE	= True		# 
	
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
	
	signal.signal(signal.SIGINT, signal_handler)
	#print 'Press Ctrl+C to exit'
	
	
	
	if DEBUG:
		print "-> Starting Client <-"
	
	try:
		
		#Main object used for sharing
		hub = dict()

		#Starts the Storage Handler
		sh = StorageHandler(hub)
		hub["STORAGE HANDLER"] = sh
		if DEBUG:
			print "Storage is ON"

		#Start Temperature/Humidity Sensor
		th = TempHumid(hub)
		th.start()
		hub["TEMPERATURE"] = th
		hub["HUMIDITY"] = th
		if DEBUG:
			print "T/H sensor is ON"

		#Start Luminosity Sensor
		lux = TSL2561(hub)
		lux.start()
		hub["LUMINOSITY"] = lux
		if DEBUG:
			print "LUX sensor is ON"
		
		#Start Current Sensor
		watt = ADS1115(hub)
		watt.start()
		hub["CURRENT"] = watt
		if DEBUG:
			print "CURRENT sensor is ON"

		#Starts Wifi Detector
		wifi = WifiDetector(hub)
		wifi.start()
		hub["WIFI"] = wifi
		wifi.track_device('40:B0:FA:C7:A1:EB')
		wifi.track_device('CC:C3:EA:0E:23:8F')
		if DEBUG:
			print "WIFI sensor is ON"
		
		#Starts BT Detector
		bt = BTDetector(hub)
		bt.start()
		bt.track_device('40:B0:FA:3D:5F:08')
		hub["BLUETOOTH"] = bt
		if DEBUG:
			print "BT sensor is ON"

		#Starts Relay
		r = Relay(hub)
		hub["RELAY"] = r
		if DEBUG:
			print "Relays are ON"
		
		#Starts LCD
		lcd = LCD(hub)
		lcd.start()
		hub["LCD"] = lcd
		if DEBUG:
			print "LCD sensor ON"

		#Starts The MQTT Listener
		mqtt = MQTTC(hub)
		mqtt.start()
		hub["PUBLISHER"] = mqtt
		if DEBUG:
			print "MQTT Publisher is ON"
		
		#Starts the Scheduler Manager
		sm = ScheduleManager(hub)
		sm.start()
		hub["SCHEDULE MANAGER"] = sm
		if DEBUG:
			print "Scheduler Manager started automation"
		
		#Starts Web Server
		#Must be last (Blocking)
		if WEB_INTERFACE:
			wh = WebHandler(hub)
			wh.start()
			hub["WEB"] = wh
			if DEBUG:
				print "Web interface started"
		
		while True:
			sleep(4)
			print hub["TEMPERATURE"].getTemperature()
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





