#!/usr/bin/env python
"""Configures the B.A.T.M.A.N network between the PI nodes"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import random
from time import sleep

#Vars
MAC_Address = (
	("b8:27:eb:60:57:67", "Pi1", "10.0.0.1", "172.20.126.1"),
	("B8:27:EB:20:C0:BA", "Pi2", "10.0.0.2", "172.20.126.2"),
	("B8:27:EB:34:8A:7A", "Pi3", "10.0.0.3", "172.20.126.3"),
	("b8:27:eb:d1:19:df", "Pi4", "10.0.0.4", "172.20.126.4"),
	("b8:27:eb:aa:e9:d2", "Pi5", "10.0.0.5", "172.20.126.5"),
	("b8:27:eb:10:4a:74", "Pi6", "10.0.0.6", "172.20.126.6")
	)

MyMAC = os.popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'").read().lower().split('\n')[0]

batnet_ip = "10.0.0.20"
priv_ip = "172.20.126.20"

for mac, pi, ip, p_ip in MAC_Address:
	if MyMAC in mac.lower():
		print "You are "+pi
		print "Your adress is "+ip+" and "+p_ip
		batnet_ip = ip
		priv_ip = p_ip
		break

#sleep(15)
os.popen("sudo modprobe -r batman-adv")
sleep(1)
os.popen("sudo modprobe batman-adv")
sleep(1)
os.popen("sudo iw dev wlan0 del")
sleep(1)
os.popen("sudo iw phy phy0 interface add me0 type ibss")
sleep(1)
os.popen("sudo ifconfig me0 mtu 1532")
os.popen("sudo iwconfig me0 txpower 20")
os.popen("sudo iwconfig me0 txpower fixed")
os.popen("sudo iwconfig me0 rts 250")
#os.popen("sudo iwconfig me0 enc off")
os.popen("sudo iwconfig me0 key FEFA88C0BE")
os.popen("sudo iwconfig me0 mode ad-hoc essid BatmanNetwork ap any channel 1")
sleep(1)
os.popen("sudo batctl if add me0")
sleep(1)
os.popen("sudo ifconfig me0 up")
sleep(1)
os.popen("sudo ifconfig me0 "+batnet_ip+"/24 up")
sleep(1)

#Enable the brige if this device is the gateway
if batnet_ip is "10.0.0.1":
	os.popen("sudo brctl addbr br0")
	os.popen("sudo brctl stp br0 off")
	os.popen("sudo brctl addif br0 bat0")
	os.popen("sudo brctl addif br0 eth0")
	os.popen("sudo ifconfig eth0 0.0.0.0 up")
	os.popen("sudo ifconfig bat0 0.0.0.0 up")
	#os.popen("sudo ifconfig br0 hw ether b8:27:eb:60:57:67")
	os.popen("sudo ifconfig br0 "+priv_ip+"/24 up")
else:
	#Set wired ip
	os.popen("sudo brctl addbr br0")
	os.popen("sudo brctl stp br0 off")
	os.popen("sudo brctl addif br0 bat0")
	os.popen("sudo brctl addif br0 eth0")
	os.popen("sudo ifconfig br0 "+priv_ip+"/24 up")
	
os.popen("sudo sed -i 's/nameserver 8.8.8.8//g' /etc/resolv.conf")
os.popen("sudo route add default gw 172.20.126.254")
os.popen("sudo sh -c 'echo nameserver 8.8.8.8 >> /etc/resolv.conf'")
os.popen("sudo alfred -i me0 -m &")
os.popen("sudo batadv-vis -i me0 -s &")	
os.popen("sudo /opt/peromas/altbeacon_transmit_peromas '"+priv_ip+"'")
sleep(20)
os.popen("sudo sh -c 'echo nameserver 8.8.8.8 >> /etc/resolv.conf'")
