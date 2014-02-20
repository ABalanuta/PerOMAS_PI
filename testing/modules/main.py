#!/usr/bin/python
from time import sleep
from datetime import datetime
from sensors.temp_humid.TempHumidFake import TempHumidFake
from sensors.wifi_detect.WifiLocation import WifiDetector
#from web.app import app
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
		


##Executed if only is the main app		
if __name__ == '__main__':	
	
	if DEBUG:
		print "Starting main"
	
	try:
		hub = Hub()
	
		#Start Temperature/Humidity Sensor
		th = TempHumidFake(hub)
		th.start()
		hub.temp_humid = th
		
		#Starts Wifi Detector
		wifi = WifiDetector(hub)
		wifi.start()
		hub.wifi = wifi
		wifi.track('40:B0:FA:C7:A1:EB')
		
	
		while True:
			sleep(2)
			print hub.temp_humid.temp
			print hub.wifi.findAll()
			
	except:
		th.stop()
		wifi.stop()
		
		try:
			raise
		except KeyboardInterrupt:
			print "\n"
		
		
		
	
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






