#!/usr/bin/python
from time import sleep
from datetime import datetime
from sensors.temp_humid.TempHumid import TempHumid
from sensors.wifi_detect.WifiLocation import WifiDetector
from sensors.bt_detect.BTDetector2 import BTDetector
from interaction.lcd.LCDmenu import LCD
from web.web import WebManager
#

#Debbuging Mode
DEBUG = 1


#Used to interconect all Modules
class Hub():
	
	def __init__(self):
		self.temp_humid = None
		self.lcd = None
		self.wifi = None
		self.bt = None
		self.lcd = None
		


##Executed if only is the main app		
if __name__ == '__main__':	
	
	if DEBUG:
		print "Starting main"
	
	try:
		
		#Main object used for sharing
		hub = Hub()
	
		#Start Temperature/Humidity Sensor
		th = TempHumid(hub)
		th.start()
		hub.temp_humid = th
		if DEBUG:
			print "T/H sensor ON"
			
		#Starts LCD
		lcd = LCD(hub)
		lcd.start()
		hub.lcd = lcd
		if DEBUG:
			print "LCD sensor ON"
			
		#Starts Wifi Detector
		#wifi = WifiDetector(hub)
		#wifi.start()
		#hub.wifi = wifi
		#wifi.track('40:B0:FA:C7:A1:EB')
		#if DEBUG:
		#	print "WIFI sensor ON"
		
		#Starts BT Detector
		#bt = BTDetector(hub)
		#bt.start()
		#hub.bt = bt
		#if DEBUG:
		#	print "BT sensor ON"
		
		
		
		
		#Starts Web Server
		#MUST BE LAST (blocks the thread)
		#wm = WebManager(hub)
		#wm.start()
		
		while True:
			sleep(4)
			
			# TEmp and Humid
			print "#Temp and Humidity"
			print "\t", hub.temp_humid.temp, "C ", hub.temp_humid.humid, "%"
			
			# Detected BT devices
			#print "#Last seen BT devices"
			#for device in hub.bt.seen_devices:
			#	print "\t", device["Name"], "seen ", (datetime.now() - device["Last seen"]).total_seconds(), "seconds ago !"
			#print "\n"
			
			
			#print hub.wifi.findAll()
				
	except:
		raise
		
	finally:
		if hub.temp_humid:
			hub.temp_humid.stop()
			
		if hub.wifi:
			hub.wifi.stop()

		if hub.bt:
			hub.bt.stop()
			
		if hub.lcd:
			hub.lcd.stop()
		
		
		
		
	
	#thermo = TermoHumid()
	#thermo.start()

	#sensorList = []
	#sensorList.append(thermo)


	#lcd = LCD(sensorList)
	#lcd.start()

	

	#web = None
	#wifi = None


	#for x in toStart:
		
	#	if x == 'web':
	#		if DEBUG:
	#			print "Start web"
	#		web = app
	#		web.run(host='0.0.0.0', debug = True, use_reloader=False)
	#	
	#	elif x == 'wifi':
	#		if DEBUG:
	#			print "Start wifi"
	#		wifi = WifiDetector()
	#		wifi.start()
	#		wifi.track('40:B0:FA:C7:A1:EB')

	#sleep(100)
	
	#TODO for x in toStart:
		#stop





