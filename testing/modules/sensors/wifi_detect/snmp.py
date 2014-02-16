import netsnmp
import socket
import threading
from time import sleep

DEBUG = 0
#APs ip Range 172.20.3.1-60
ipRange = ('172.20.3.', 1, 90)
scanDelay = 5 #seconds

#Converts the deciaml representation to hexadecimal
def get_mac(var):
	mac = var.split('.')
	mac = mac[-6:]
	for x in range(0, len(mac)):
		char = hex(int(mac[x])).split('x')[1].upper()
		if len(char) == 1:
			mac[x] = '0'+char
		else:
			mac[x] = char
	return mac[0]+':'+mac[1]+':'+mac[2]+':'+mac[3]+':'+mac[4]+':'+mac[5]
	
	
class ResolveDns(threading.Thread):
	
	def __init__(self, ip):
		threading.Thread.__init__(self)
		self.ip = ip
		self.dnsname = None

	def run(self):
		try:
			name, alias, addresslist = socket.gethostbyaddr(self.ip)
			self.dnsname = name.split('.')[0].upper()
		except socket.error:
			self.dnsname = None

def get_dns_name(ip):

	dns = ResolveDns(ip)
	dns.start()
	#timeout after .7 second
	dns.join(0.7)
	
	if dns.dnsname:
		return str(dns.dnsname)
	else:
            return None

def get_associated(ip):
	
	oid = '.1.3.6.1.4.1.9.9.273.1.2.1.1.14'
	
	dns_name = get_dns_name(ip)
	
	if dns_name:
		if DEBUG:
			print "Found AP "+dns_name
		
		session = netsnmp.Session( DestHost=ip, Version=2, Community='public',Timeout=10000, Retries=1, UseNumeric=1)
		session.UseLongNames = 1
		vars = netsnmp.VarList( netsnmp.Varbind(oid) )
		session.walk(vars)
		
		list = []
		for var in vars:
			mac = get_mac(var.tag+"."+var.iid)
			list.append((mac, var.val, dns_name))
		return list
			
	else:
		if DEBUG:
			print "Did not Found AP"
		return []


class WifiDetector(threading.Thread):
	
	def __init__(self, macList):
		if DEBUG:
			print "WifiDetector.init()"
		threading.Thread.__init__(self)
		self.stopped = True
		self.detectedList = []
		self.searchList = macList
		self.presentList = []
	
	def stop(self):
		if DEBUG:
			print "WifiDetector.stop()"
		self.stopped = True
	
	def run(self):
		if DEBUG:
			print "WifiDetector.run()"
		self.stopped = False
		count = 11
		while not self.stopped:
			if count > scanDelay:
				self.update()
				count = 0
			else:
				count += 1
				sleep(1)
				
	def update(self):
		if DEBUG:
			print "WifiDetector.update()"
		
		newList = []
		for x in range(int(ipRange[1]), int(ipRange[2])+1):
			ip = ipRange[0]+str(x)
			l = get_associated(ip)
			if len(l) > 0:
				newList += l
			#sleep(0.05)
		self.detectedList = newList
		
		if DEBUG:
			for x in newList:
				print x
			print "Len:",len(newList)
		
		self.updatePresentList()
		
		
	def updatePresentList(self):
		
		newPresentList = []
		for x in self.searchList:
			for y in self.detectedList:
				if x == y[0]:
					if DEBUG:
						print x, "is at ", y[2]
					newPresentList += [(x, y[2])]
					#break
					
		self.presentList = newPresentList
		if not DEBUG:
			print self.presentList	
	
		
##Executed if only is the main app		
if __name__ == '__main__':

	macList = ['40:B0:FA:C7:A1:EB']
	
	wd = WifiDetector(macList)
	
	try:
		wd.start()
		sleep(300)
		wd.stop()
	except KeyboardInterrupt:
		wd.stop()
	
		
		
		
		
