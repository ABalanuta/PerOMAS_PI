import netsnmp
import socket
import threading
import time

#Converts the deciaml representation to hexadecimal
def get_mac(var):
	split = var.split('.')
	mac = split[-6:]
	#print mac
	for x in range(0, 6):

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
	#timeout after 1 second
	dns.join(0.5)
	
	if dns.dnsname:
		return "\n\n#####$"+str(dns.dnsname)
	else:
		return "Error"

def get_associated(ip):
	#IP address
	#ip = 'L_0-BIB3'
	#Associated Clientes OID
	oid = '.1.3.6.1.4.1.9.9.273.1.2.1.1.14'

	session = netsnmp.Session( DestHost=ip, Version=2, Community='public',Timeout=10000, Retries=1, UseNumeric=1)
	#session.UseLongNames = 1
	vars = netsnmp.VarList( netsnmp.Varbind(oid) )
	session.walk(vars)
	
	print get_dns_name(ip)
	#try:
	for var in vars:
		mac = get_mac(var.tag)
		print mac, var.val
	#e
		
		
##Executed if only is the main app		
if __name__ == '__main__':

	for x in range(50, 90):
		get_associated('172.20.3.'+str(x))
		time.sleep(0.25)
		
		
		
		
		
