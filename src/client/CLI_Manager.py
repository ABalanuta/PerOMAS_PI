#!/usr/bin/env python

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


import subprocess
import json
import platform
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

	def get_local_IP(self):
		self.ip = "0.0.0.0"
		if 'armv6l' in platform.uname():
			try:
				p = subprocess.Popen("sudo ifconfig br0; sudo ifconfig bat0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				lines = p.stdout.readlines()
				for line in lines:
					if "inet addr:" in line:
						self.ip = str(line.split()[1].split(':')[1])
						return self.ip
			except:
				return self.ip
		return self.ip

#Runs only if called
if __name__ == "__main__":


	cm = CLI_Manager(None)
	cm.start()
	#sleep(1)
	print cm.getBatmanNodes()
	cm.stop()
