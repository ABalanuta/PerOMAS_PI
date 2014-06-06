all: profile update i2c gpio temp_humid_sensor startup pubsub network bluetooth snmp web mesh mysql hostname tft boot reboot

profile:
	git config --global user.email AliensGoo@users.noreply.github.com
	git config --global user.name AliensGoo

update:
	sudo aptitude update -y
	sudo aptitude upgrade -y
	sudo aptitude install vim git tmux screen htop -y
gpio:
	sudo apt-get install python-dev -y
	sudo apt-get install python-rpi.gpio -y
i2c:
	##I2c Tools
	sudo cp modules /etc/modules
	sudo cp raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf
	sudo aptitude install python-smbus i2c-tools -y

tft:
	wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-bin-adafruit.deb
	wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-dev-adafruit.deb
	wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-doc-adafruit.deb
	wget http://adafruit-download.s3.amazonaws.com/libraspberrypi0-adafruit.deb
	wget http://adafruit-download.s3.amazonaws.com/raspberrypi-bootloader-adafruit-112613.deb
	sudo dpkg -i -B *.deb
	sudo mv /usr/share/X11/xorg.conf.d/99-fbturbo.conf /tmp/99-fbturbo.conf
	sudo cp adafruit.conf /etc/modprobe.d/adafruit.conf
	sudo mkdir /etc/X11/xorg.conf.d
	sudo cp 99-calibration.conf /etc/X11/xorg.conf.d/99-calibration.conf	
	sudo cp 95-stmpe.rules /etc/udev/rules.d/95-stmpe.rules
	sudo cp modules /etc/modules
	#sudo rmmod stmpe_ts; sudo modprobe stmpe_ts
	sudo apt-get install evtest tslib libts-bin -y
	#sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate

pubsub:
	sudo apt-get install python-mosquitto -y

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
	sudo aptitude install bluez bluez-tools python-gobject python-gobject-2 -y

snmp:
	sudo aptitude install snmp libsnmp-python python-pysnmp2 python-pysnmp-common -y

web:
	sudo aptitude install python-pip -y
	sudo pip install flask
	sudo pip install flask-wtf
	sudo pip install Flask-Cache
	sudo pip install flask-compress
	sudo pip install Flask-Login
	sudo pip install tornado
	#pip install flask-login
	#pip install flask-openid
	#pip install sqlalchemy

mesh:
	sudo aptitude install htop ntp batctl batctl bridge-utils iw wireless-tools iperf -y

boot:
	sudo cp StartUP /etc/init.d/
	sudo update-rc.d StartUP remove
	sudo update-rc.d StartUP defaults
	sudo mkdir /opt/peromas -p
	sudo cp start_batman.py /opt/peromas/	

hostname:
	sudo python change_host.py

gateway:
	cd /tmp/; wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key; sudo apt-key add mosquitto-repo.gpg.key
	cd /etc/apt/sources.list.d/; sudo wget http://repo.mosquitto.org/debian/mosquitto-stable.list
	sudo apt-get update -y
	sudo apt-get install mosquitto -y
	
mysql:
	sudo aptitude install mysql-client mysql-server python-mysqldb -y
	echo "Optimizing MySQL"
	sudo cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak
	sudo cp my.cnf /etc/mysql/my.cnf
	sudo service mysql restart

reboot:
	echo "System will rebootn in 10"
	sleep 10
	sudo reboot
