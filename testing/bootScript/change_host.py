import os
import random

#Vars
MyPI = "ChangeMe-ls"+str(random.randint(0, 99))
MAC_Address = (("B8:27:EB:60:57:67", "Pi1"), ("B8:27:EB:34:8A:7A","Pi3"), ("B8:27:EB:20:C0:BA", "Pi2"))

MyMAC = os.popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'").read().lower()

for mac, pi in MAC_Address:
	if mac.lower() is MyMAC:
		MyPI = pi

os.popen("sudo echo "+pi+" > /etc/hostname")
