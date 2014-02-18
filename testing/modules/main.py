#!/usr/bin/python

from sensors.temp_and_humid.sensTempHum import TermoHumid

from sensors.wifi_detect.wifiLocation import WifiDetector

from web.app import app

#from interaction.lcd.lcdmenu import *

from time import sleep

from datetime import datetime

DEBUG = 1

global thermo
global lcd
global web
global wifi

##Executed if only is the main app		
if __name__ == '__main__':

	#thermo = TermoHumid()
	#thermo.start()

	#sensorList = []
	#sensorList.append(thermo)


	#lcd = LCD(sensorList)
	#lcd.start()

	toStart = ['web', 'wifi']

	web = None
	wifi = None


	for x in toStart:
		
		if x == 'web':
			if DEBUG:
				print "Start web"
			web = app
			web.run(host='0.0.0.0', debug = True, use_reloader=False)
		
		elif x == 'wifi':
			if DEBUG:
				print "Start wifi"
			wifi = WifiDetector()
			wifi.start()
			wifi.track('40:B0:FA:C7:A1:EB')

	sleep(100)
	
	#TODO for x in toStart:
		#stop






