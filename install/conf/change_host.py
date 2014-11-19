#!/usr/bin/env python
"""Changes the hostname of the raspberryPi based on the MAC"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import random

#Vars
MyPI = "ChangeMe-ls"+str(random.randint(0, 99))

MAC_Address = (
	("b8:27:eb:60:57:67", "Pi1"),
	("B8:27:EB:20:C0:BA", "Pi2"),
	("B8:27:EB:34:8A:7A", "Pi3"),
	("b8:27:eb:d1:19:df", "Pi4"),
	("b8:27:eb:aa:e9:d2", "Pi5"),
	("b8:27:eb:10:4a:74", "Pi6")
	)

MyMAC = os.popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'").read().lower().split('\n')[0]

for mac, pi in MAC_Address:
	if MyMAC in mac.lower():
		print "You are "+pi
		MyPI = pi
		break

os.popen("sudo hostname " + MyPI)

print "You Need to reboot the Pi"
