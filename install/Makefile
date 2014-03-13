all: profile update i2c temp_humid_sensor startup network bluetooth snmp web

profile:
	git config --global user.email AliensGoo@users.noreply.github.com
	git config --global user.name AliensGoo

update:
	sudo aptitude update -y
	sudo aptitude upgrade -y

i2c:
	##I2c Tools
	sudo cp modules /etc/modules
	sudo cp raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf
	sudo aptitude install python-smbus i2c-tools -y

temp_humid_sensor:
	#wiringPi Library AutoInstall
	sudo apt-get install git-core -y
	rm -rf wiringPi
	git clone git://git.drogon.net/wiringPi
	cd wiringPi; sudo ./build
	gpio readall
	rm -rf wiringPi

startup:
	sudo cp StartUP /etc/init.d/StartUP
	cd /etc/init.d/;sudo chmod +x StartUP;sudo update-rc.d StartUP defaults

network:
	sudo aptitude install iw -y
	#sudo aptitude install firmware-realtek -y
	
bluetooth:
	sudo aptitude install bluez  bluez-tools python-gobject python-gobject-2 -y

snmp:
	sudo aptitude install snmp libsnmp-python python-pysnmp2 python-pysnmp-common -y

web:
	sudo aptitude install python-pip -y
	sudo pip install flask
	sudo pip install flask-wtf
	#pip install flask-login
	#pip install flask-openid
	#pip install sqlalchemy
