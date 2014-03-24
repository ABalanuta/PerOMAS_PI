import os
import random
from time import sleep

#Vars
MAC_Address = (
	("b8:27:eb:60:57:67", "Pi1", "10.0.0.1"),
	("B8:27:EB:20:C0:BA", "Pi2", "10.0.0.2"),
	("B8:27:EB:34:8A:7A", "Pi3", "10.0.0.3"),
	("b8:27:eb:d1:19:df", "Pi4", "10.0.0.4"),
	("b8:27:eb:aa:e9:d2", "Pi5", "10.0.0.5"),
	("b8:27:eb:10:4a:74", "Pi6", "10.0.0.6")
	)

MyMAC = os.popen("ifconfig eth0 | grep HWaddr | awk '{print $5}'").read().lower().split('\n')[0]

batnet_ip = "0.0.0.0"

for mac, pi, ip in MAC_Address:
	if MyMAC in mac.lower():
		print "You are "+pi
		print "Your adress is "+ip
		batnet_ip = ip		
		break

sleep(15)
os.popen("sudo modprobe batman-adv")
sleep(2)
os.popen("sudo iw dev wlan0 del")
sleep(2)
os.popen("sudo iw phy phy0 interface add me0 type ibss")
sleep(2)
os.popen("sudo ifconfig me0 mtu 1528")
sleep(2)
os.popen("sudo iwconfig me0 enc off")
sleep(2)
os.popen("sudo iwconfig me0 mode ad-hoc essid BatmanNetwork ap any channel 1")
sleep(2)
os.popen("sudo batctl if add me0")
sleep(2)
os.popen("sudo ifconfig me0 up")
sleep(2)
os.popen("sudo ifconfig me0 "+batnet_ip+"/24 up")
sleep(2)

#Enable the brige if this device is the gateway
if batnet_ip is "10.0.0.1":
	os.popen("sudo brctl addbr br0")
	os.popen("sudo brctl stp br0 off")
	os.popen("sudo brctl addif br0 bat0")
	os.popen("sudo brctl addif br0 eth0")
	os.popen("sudo ifconfig bat0 0.0.0.0 up")
	os.popen("sudo ifconfig eth0 0.0.0.0 up")
	os.popen("sudo ifconfig br0 hw ether b8:27:eb:60:57:67")
	os.popen("sudo dhclient br0")

#Get DHCP IP from the wired vlan
os.popen("sudo dhclient bat0")


