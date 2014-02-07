all: install

install:
	#I2C
	sudo cp modules /etc/modules
	sudo cp raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf
	sudo apt-get install python-smbus i2c-tools
