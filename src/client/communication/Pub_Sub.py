#!/usr/bin/env python
"""Pub Sub Comunication between Nodes"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import mosquitto
from threading import Thread
from time import sleep, clock


class MQTTC(Thread):

	DEBUG		= False
	BROKER_IP	= "10.0.0.1"
	ZONE		= "2N11"		#Subscribe Wildcard

	def __init__(self, hub):
		Thread.__init__(self)
		self.hub = hub
		self.stopped = True
		self.connected = False
		self.hostname = os.uname()[1]
		self._mqttc = mosquitto.Mosquitto(self.hostname)
		self._mqttc.on_message = self.mqtt_on_message
		self._mqttc.on_connect = self.mqtt_on_connect
		self._mqttc.on_publish = self.mqtt_on_publish
		self._mqttc.on_subscribe = self.mqtt_on_subscribe
		self._mqttc.on_disconnect = self.mqtt_on_disconnect

	def mqtt_on_connect(self, mqttc, _userdata, rc):

		if rc == 0:
			if self.DEBUG:
				print "--Connected ok"
			self.connected = True
		else:
			print "--Connect Error: "+str(rc)

	def mqtt_on_message(self, mqttc, _userdata, msg):
		print str(msg.qos)+" "+msg.topic+" "+str(msg.payload)

	def mqtt_on_publish(self, mqttc, _userdata, mid):
		pass
		#print("mid: "+str(mid))

	def mqtt_on_subscribe(self, mqttc, _userdata, mid, granted_qos):
		pass
		#print "Subscribed: "+str(mid)+" "+str(granted_qos) 

	def mqtt_on_log(self, mqttc, _userdata, level, string):
		print string

	def mqtt_on_disconnect(self, mqttc, _userdata, rc):
		if self.DEBUG:
			print "--Disconected !!!"
		self.connected = False

	def publish(self, topic, payload, qos):
		self._mqttc.publish(self.ZONE+"/"+self.hostname+"/"+topic, payload, qos)

	def stop(self):
		print "MQTT Stoped1"
		self.stopped = True
		self._mqttc.disconnect()
		if self.DEBUG:
			print "MQTT Stoped"
	
	def run(self):
		self.stopped = False
		self._mqttc.connect(self.BROKER_IP, 1883)

		while not self.stopped:
			self.update()
			sleep(0.2)
			
	def update(self):
		rc = self._mqttc.loop()
		if rc != 0:	#Error Raised
			self.stopped = True
			self.connected = False


#Runs only if called
if __name__ == "__main__":


	client = MQTTC(None)
	client.start()

	while not client.connected:
		sleep(0.1)
	try:
		
		while True:
			client.publish("Clock", str(clock()), 2)
			sleep(2)
	
	except:
		client.stop()
		print "Stoped"