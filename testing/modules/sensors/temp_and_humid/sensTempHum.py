from time import sleep
import signal
import subprocess
import sys
from threading import Thread
from datetime import datetime

#Temp and Humid Sensor Data Pin
dhtpin = 7


class TermoHumid(Thread):

	temp = 0.0
	humid = 0.0
	lastUpdate = 0

	def __init__(self):
		self.stopped = False
		Thread.__init__(self)
		self.update()
	
	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			self.update()

	def update(self):
		values = subprocess.check_output(["./aux/rpi_dht", str(dhtpin)])
		for line in values.split('\n'):
			if "Humidity" in line:
				#print str(datetime.now()), line
				parts = line.split(' ')
				self.humid = parts[5]
				self.temp = parts[9]
				self.lastUpdate = datetime.now()
				break

started = datetime.now()


print "#TEST#"
print "#Starting#"
d = TermoHumid()
d.start()


while True:	
	print "Runtime:", str(d.lastUpdate-started), "\tTemp:", d.temp, "\tHumid:", d.humid
	sleep(2)

d.stop()
print "#Sttoped#\n\n"