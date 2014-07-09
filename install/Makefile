all: echo_options

echo_options:
	@echo '# # Options # #'
	@echo
	@echo '0: #// Add User/Keys INFO'
	@echo '1: #// Pre-install'
	@echo '2: #// Nostro Firmware with pitft and touch suport'
	@echo '3: #// Install Software'
	@echo '4: #// Install Addicional Software (Gateway Only)'
	@echo '5: #// Configuration Variables'
	@echo '6: #// Test touchscreen'
	@echo '7: #// Test x'
	@echo '8: #// Backup MySQL Database'
	@echo '9: #// Restore MySQL Database'
	@echo


0: #// Add User/Keys INFO
	@echo
	@echo 'ssh pi@piX'
	@echo 'pass:raspberry'
	@echo
	@echo 'sudo su'
	@echo 'adduser artur-adm'
	@echo 'pass:xxxxx'
	@echo
	@echo "sudo sed -i 's/pi/artur-adm/' /etc/sudoers"
	@echo
	@echo 'exit'
	@echo 'exit'
	@echo
	@echo '//Copy Key'
	@echo 'ssh-copy-id artur-adm@piX'
	@echo
	@echo 'ssh artur-adm@piX'
	@echo 'sudo deluser pi'

	@echo
	@echo 'Option 0 DONE'
	@echo



1: #// Pre-install

	#//Update & Upgrade
	sudo aptitude purge wolfram-engine omxplayer scratch zenity midori -y
	
	#sudo apt-mark hold raspberrypi-bootloader
	sudo apt-get update -y 
	sudo apt-get upgrade -y

	@echo
	@echo 'Reboot the System Manually'

	@echo
	@echo 'Option 1 DONE'
	@echo


2: #// Nostro Firmware with pitft and touch suport

	#Firmware for the pitft
	#https://github.com/notro/rpi-firmware
	sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update
	sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update
	#sudo REPO_URI=https://github.com/notro/rpi-firmware BRANCH=builtin rpi-update

	@echo
	@echo 'Reboot the System Manually'

	@echo
	@echo 'Option 2 DONE'
	@echo


3: #// Install Software

	@echo 'Aux'
	sudo aptitude install git vim zsh tmux screen htop ntp ntpdate -y
	@echo

	@echo 'GPIO'
	sudo aptitude install python-dev python-rpi.gpio -y
	@echo

	@echo 'I2C'
	sudo aptitude install python-smbus i2c-tools -y
	@echo

	@echo 'Mosqitto'
	sudo aptitude install python-mosquitto -y
	@echo

	@echo 'Bluetooth'
	sudo aptitude install bluez bluez-tools python-gobject python-gobject-2 -y
	@echo

	@echo 'SNMP'
	sudo aptitude install snmp libsnmp-python python-pysnmp4 python-pysnmp-common -y
	@echo

	@echo 'WEB'
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
	@echo

	@echo 'Mesh'
	sudo aptitude install batctl bridge-utils iw wireless-tools iperf -y
	@echo

	@echo 'MySQL'
	sudo aptitude install mysql-client mysql-server python-mysqldb -y
	@echo "Optimizing MySQL"
	sudo cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak
	sudo cp conf/my.cnf /etc/mysql/my.cnf
	sudo service mysql restart
	@echo

	@echo
	@echo 'Option 3 DONE'
	@echo


4: #// Install Addicional Gateway Software

	#// Mosquitto Server
	cd /tmp/; wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key; sudo apt-key add mosquitto-repo.gpg.key
	cd /etc/apt/sources.list.d/; sudo wget http://repo.mosquitto.org/debian/mosquitto-stable.list
	sudo aptitude update -y
	sudo aptitude install mosquitto -y
	@echo

	@echo
	@echo 'Option 4 DONE'
	@echo


5:	#// Configuration Variables

	#//Set git Variables
	git config --global user.email AliensGoo@users.noreply.github.com
	git config --global user.name AliensGoo
	@echo

	#// remove backlight timeout
	sudo sed -i 's/BLANK_TIME=30/BLANK_TIME=0/' /etc/kbd/config
	@echo

	#// add event rule
	sudo cp conf/95-stmpe.rules /etc/udev/rules.d/95-stmpe.rules
	@echo

	#// touchscreen calibration values
	sudo mkdir /etc/X11/xorg.conf.d; true
	sudo cp conf/99-calibration.conf /etc/X11/xorg.conf.d/
	@echo

	#//bugfix X would not start wthout it
	sudo sed -i 's/fb0/fb1/' /usr/share/X11/xorg.conf.d/99-fbturbo.conf
	@echo


	#// Auto Load Modules
	sudo cp conf/modules /etc/modules
	@echo

	#// Remove Blacklist of I2C and spi
	sudo sed -i 's/blacklist\ i2c-bcm2708/#blacklist\ i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
	sudo sed -i 's/blacklist\ spi-bcm2708/#blacklist\ spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
	@echo

	#// Startup Script
	sudo cp conf/StartUP /etc/init.d/StartUP
	cd /etc/init.d/; sudo chmod +x StartUP
	sudo update-rc.d StartUP remove; true
	sudo update-rc.d StartUP defaults; true
	@echo

	#//Aux Scripts
	sudo mkdir /opt/peromas -p; true
	sudo cp conf/start_batman.py /opt/peromas/
	@echo

	#// Ajust TimeZone
	sudo dpkg-reconfigure tzdata

	#// NTP
	sudo cp conf/crontab /etc/crontab
	sudo /etc/init.d/cron restart
	
	#// MOTD
	sudo cp conf/motd /etc/motd
	
	#//oh-my-zsh
	curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh
	@echo USER PASSWORD
	chsh -s /bin/zsh
	cp conf/zshrc ~/.zshrc
	
	#
	#// Change Hostname
	sudo python conf/change_host.py

	@echo 'Reboot the System Manually'

	@echo
	@echo 'Option 5 DONE'
	@echo

6: #// Test touchscreen

	@echo 'Test Soft'
	sudo apt-get install evtest tslib libts-bin -y
	@echo

	#// Touchscreen
	sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate
	sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_test

	@echo
	@echo 'Option 6 DONE'
	@echo

7: #// Test X
	
	FRAMEBUFFER=/dev/fb1 startx

8: #// Backup MySQL
	sudo mysqldump -uroot -p3O7DCWP2HLR01471G9PZQ6U7X PeromasDB > /tmp/PeromasDB.sql
	scp /tmp/PeromasDB.sql ist168206@sigma.ist.utl.pt:~

9: #// Restore MySQL
	scp ist168206@sigma.ist.utl.pt:~/PeromasDB.sql /tmp/PeromasDB.sql
	sudo mysql-uroot -p3O7DCWP2HLR01471G9PZQ6U7X PeromasDB < /tmp/PeromasDB.sql
