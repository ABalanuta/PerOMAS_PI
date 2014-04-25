#!/usr/bin/env python
"""?????????"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import mosquitto
from time import sleep, clock

BROKER_IP	= "10.0.0.1"



def on_message(obj, msg):
	print msg.payload
    #print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)

    #mosq.publish('pong', "Thanks", 0)

def on_publish(obj, mid):
    pass

def on_connect(rc):
	if rc == 0:
		print "--Connected ok"
	else:
		print "--Connect Error: "+str(rc)

def on_disconnect(obj):
	print "--Disconected !!!"


cli = mosquitto.Mosquitto("pi1")

cli.on_message = on_message
cli.on_publish = on_publish
cli.on_connect = on_connect
cli.on_disconnect = on_disconnect

cli.connect(BROKER_IP, 1883, 60)

#cli.subscribe("$SYS/#", 2)
cli.subscribe("nagios/#", 2)
cli.subscribe('pong', 2)



sleep(0.5)



cli.publish('pong', "Thanks", 2)
cli.publish('pong', "cenas", 2)
cli.publish('nagios/#', "AAAAA", 2)

cli.publish('nagios/#', "cenas", 2)

sleep(0.5)

while cli.loop() == 0:
	pass