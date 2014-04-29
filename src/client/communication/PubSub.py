#!/usr/bin/env python
"""?????????"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import mosquitto
from threading import Thread
from time import sleep, clock


class MyMQTTClass(Thread):

	BROKER_IP	= "10.0.0.1"
	ZONE		= "2N11/"		#Subscribe Wildcard

	def __init__(self,gateway=False):
		Thread.__init__(self)
		self.gateway = gateway
		self.stopped = True
		self.hostname = os.uname()[1]
		self._mqttc = mosquitto.Mosquitto(self.hostname)
		self._mqttc.on_message = self.mqtt_on_message
		self._mqttc.on_connect = self.mqtt_on_connect
		self._mqttc.on_publish = self.mqtt_on_publish
		self._mqttc.on_subscribe = self.mqtt_on_subscribe
		self._mqttc.on_disconnect = self.mqtt_on_disconnect

	def mqtt_on_connect(self, mqttc, rc):
		if rc == 0:
			print "--Connected ok"
		else:
			print "--Connect Error: "+str(rc)

	def mqtt_on_message(self, mqttc, msg):
		print str(msg.qos)+" "+msg.topic+" "+str(msg.payload)

	def mqtt_on_publish(self, mqttc, mid):
		pass
		#print("mid: "+str(mid))

	def mqtt_on_subscribe(self, mqttc, mid, granted_qos):
		pass
		#print "Subscribed: "+str(mid)+" "+str(granted_qos) 

	def mqtt_on_log(self, mqttc, level, string):
		print string

	def mqtt_on_disconnect(self, mqttc):
		print "--Disconected !!!"

	def publish(self, topic, payload, qos):
		self._mqttc.publish(self.ZONE + topic, payload, qos)

	def stop(self):
		self.stopped = True
		self._mqttc.disconnect()
	
	def run(self):
		self.stopped = False
		self._mqttc.connect(self.BROKER_IP, 1883)

		if self.gateway:
			self._mqttc.subscribe(self.ZONE+"#", 0)

		while not self.stopped:
			self.update()
			
	def update(self):
		rc = self._mqttc.loop()
		if rc != 0:	#Error Raised
			self.stopped = True


#Runs only if called
if __name__ == "__main__":
	client = MyMQTTClass(gateway=True)
	client.start()

	sleep(1)
	client.publish(client.hostname+"/Temperatura", "25 C", 2)
	client.publish(client.hostname+"/Humidity", "200%", 2)
	client.publish(client.hostname+"/Lux", "400", 2)
	client.publish(client.hostname+"/BT", "Aloha", 2)
	client.publish(client.hostname+"/WIFI", "it's me Mario", 2)
	sleep(3)
	client.stop()