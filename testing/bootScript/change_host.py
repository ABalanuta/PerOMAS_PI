import os
import random

#Vars
MyPI = "ChangeMe-ls"+str(random.randint(0, 99))
MAC_Address = (("b8:27:eb:60:57:67", "Pi1"), ("B8:27:EB:34:8A:7A","Pi3"), ("B8:27:EB:20:C0:BA", "Pi2"))

MyMAC = os.popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'").read().lower().split('\n')[0]

for mac, pi in MAC_Address:
	if MyMAC in mac:
		print "YOU ARE "+pi
		MyPI = pi
		break

os.popen("sudo echo "+pi+" > /etc/hostname")
os.popen("sudo echo '127.0.0.1\t"+pi+" >> /etc/hosts")
