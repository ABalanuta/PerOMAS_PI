from time import sleep
import signal
import subprocess
import sys
from threading import Thread
from datetime import datetime

#Sensor Temp
dhtpin = 7

global temp
global humid

temp = 0.0
humid = 0.0

class Termo(Thread):      
	def __init__(self):
                self.stopped = False
		Thread.__init__(self)
	
	def stop(self):
                self.stopped = True

    	def run(self):
    		global temp
    		global humid
		while not self.stopped:
			values = subprocess.check_output(["./aux/rpi_dht", str(dhtpin)])
			#print values
			for line in values.split('\n'):
				if "Humidity" in line:
					print str(datetime.now()), line
					break
			#values = dhtreader.read(dev_type, dhtpin)
			#if values: # if not null	
			#	temp = round(values[0],4)
			#	humid = round(values[1],4)
			#	print str(datetime.now()), "Temp = {0} *C, Hum = {1} %".format(temp, humid)
			#	sleep(0.5)
			#else:
			#	print str(datetime.now()), "Failed to read from sensor!!!"
			#	sleep(1)

t = Termo()
t.start()

while True:

	try:
		sleep(.25)
		#print str(datetime.now()), "alive"

	except KeyboardInterrupt:
        	print "Bye"
        	t.stop()
		sys.exit()
