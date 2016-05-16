#!/usr/bin/env python
"""Application Main Class

Starts the different modules composing the Application
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import signal, sys
from sensors.HTU21D.HTU21D import TempHumid #Temp/Humid
from sensors.OPENWEATHERMAPAPI.OpenWeatherMapAPI import OpenWeatherMapAPI #Exterior Temp/Humid
from sensors.TSL2561.TSL2561 import TSL2561	#Lux
from sensors.ADS1115.ADS1115 import ADS1115	#Current
#from detection.WifiLocation import WifiDetector
from detection.BTDetector import BTDetector
#from interaction.lcd.LCDmenu import LCD
from interaction.pitft.tft_interface import TFT
from interaction.Relay import Relay
from interaction.SSRelay import SSRelay
#from communication.Pub_Sub import MQTTC
from web.web import *
from Scheduler_Manager import ScheduleManager
from Storage_Handler import StorageHandler
from Hybrid_Storage_Handler import HibridStorageHandler
from Logic_Engine import Logic_Engine
from CLI_Manager import CLI_Manager

##Executed if only is the main app
if __name__ == '__main__':


	DEBUG			= True		# Debug Mode
	CLI_INTERFACE	= False		#
	WEB_INTERFACE	= True		#

	def signal_handler(signal, frame):

		print 'You pressed Ctrl+C!'
		for key, value in hub.items():

			if key not in ["API KEY", "STORAGE HANDLER", "UserManager"]:
				if DEBUG:
					print "Stopping", key
				try:
					if value.stop:
						value.stop()
					print "\t\t\t\tDone"
				except:
					pass

		sys.exit(0)

    def get_local_IP():
		ip = "0.0.0.0"
            if 'armv6l' in platform.uname():
                try:
                    p = subprocess.Popen("sudo ifconfig br0; sudo ifconfig bat0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    lines = p.stdout.readlines()
                    for line in lines:
                        if "inet addr:" in line:
                            ip = str(line.split()[1].split(':')[1])
                            return self.ip
                except:
                    return ip
            return ip

	if DEBUG:
		print "\n-> Starting Client <-\n"

	try:

		#Main object used for sharing
		hub = dict()
		signal.signal(signal.SIGINT, signal_handler)
		#print 'Press Ctrl+C to exit'

		#Starts the CLI Manager
		cm = CLI_Manager(hub)
		hub["CLI MANAGER"] = cm
		if DEBUG:
			print "CLI Manager is ON"

		#Starts the Storage Handler
		sh = HibridStorageHandler(hub)
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

		#Start Extenal Temperature/Humidity Sensor
		ext_th = OpenWeatherMapAPI(hub)
		hub["EXTERNAL TEMPERATURE"] = ext_th
		hub["EXTERNAL HUMIDITY"] = ext_th
		if DEBUG:
			print "External T/H sensor is ON"


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
		#wifi = WifiDetector(hub)
		#wifi.start()
		#hub["WIFI"] = wifi
		#wifi.track_device('40:B0:FA:C7:A1:EB')
		#wifi.track_device('CC:C3:EA:0E:23:8F')
		#if DEBUG:
		#	print "WIFI sensor is ON"

		#Starts BT Detector
		bt = BTDetector(hub)
		#bt.start()
		hub["BLUETOOTH"] = bt
		#if DEBUG:
		#	print "BT sensor is ON"









		#Starts LCD
		#lcd = LCD(hub)
		#lcd.start()
		#hub["LCD"] = lcd
		#if DEBUG:
		#	print "LCD screen is ON"

		#Starts The MQTT Listener
		#mqtt = MQTTC(hub)
		#mqtt.start()
		#hub["PUBLISHER"] = mqtt
		#if DEBUG:
		#	print "MQTT Publisher is ON"

		#Starts the Scheduler Manager
		sm = ScheduleManager(hub)
		sm.start()
		hub["SCHEDULE MANAGER"] = sm
		if DEBUG:
			print "Scheduler Manager started automation"

		#Starts the Logic Engine
		le = Logic_Engine(hub)
		le.start()
		hub["LOGIC ENGINE"] = le
		if DEBUG:
			print "Logic Engine started automation"


		#Starts TFT
		tft = TFT(hub)
		tft.start()
		hub["TFT"] = tft
		if DEBUG:
			print "TFT screen is ON"


		IP = get_local_IP()
		print "My IP is: " + str(IP)


		#Starts Relay
		if IP == "172.20.126.1":
			r = SSRelay(hub)
			if DEBUG:
				print "SSRelays are ON"
		else:
			r = Relay(hub)
			if DEBUG:
				print "Relays are ON"
		hub["RELAY"] = r

		#Starts Web Server
		#Must be last (Blocking)
		if WEB_INTERFACE:

			if DEBUG:
				print "Starting Web interface"

			wh = WebHandler(hub)
			wh.start()
			hub["WEB"] = wh


	except Exception as inst:
		print "Exception"
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		raise

	print "The End"
