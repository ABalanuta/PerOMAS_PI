all: i2c temp_humid_sensor

i2c:
	##I2c Tools
	sudo cp modules /etc/modules
	sudo cp raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf
	sudo apt-get install python-smbus i2c-tools


temp_humid_sensor:
	#wiringPi Library AutoInstall
	sudo apt-get install git-core
	rm -rf wiringPi
	git clone git://git.drogon.net/wiringPi
	cd wiringPi; sudo ./build
	gpio readall
	rm -rf wiringPi
