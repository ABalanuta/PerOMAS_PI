#!/usr/bin/env python

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


import subprocess
import json
from threading import Thread
from time import sleep, localtime, time

class CLI_Manager(Thread):

	DEBUG 					= False
	SLEEP_BETWEEN_CHECKS 	= 2 		#sleeps X seconds befor cheking the need of executing any task

	def __init__(self, hub):
		Thread.__init__(self)
		self.hub = hub

	def stop(self):
		self.stopped = True

	def run(self):
		self.stopped = False

		while not self.stopped:
			self.update()
			if not self.stopped:
				sleep(self.SLEEP_BETWEEN_CHECKS)

	def update(self):
		if self.DEBUG:
			print "Update"

	def getBatmanNodes(self):
		p = subprocess.Popen("sudo batadv-vis -f json | grep router | sed 's/router/source/g' | sed 's/neighbor/target/'| sed 's/label/cost/'", \
			shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		self.proc = p
		lines = p.stdout.readlines()
		retList = []
		for line in lines:
			retList.append(json.loads(line))
		return retList


#Runs only if called
if __name__ == "__main__":


	cm = CLI_Manager(None)
	cm.start()
	#sleep(1)
	print cm.getBatmanNodes()
	cm.stop()
