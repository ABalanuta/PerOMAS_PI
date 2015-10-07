all: echo_options

echo_options:
	@echo '# # Options # #'
	@echo
	@echo '1: #// Pre-install'
	@echo '2: #// Install Software'
	@echo '4: #// Install Addicional Software (Gateway Only)'
	@echo '5: #// Configuration Variables'
	@echo '6: #// Test touchscreen'
	@echo '7: #// Test x'
	@echo '8: #// Backup MySQL Database'
	@echo '9: #// Restore MySQL Database'
	@echo '10: #// Update Nodes from git and RESTART them'
	@echo

1: #// Pre-install

	#disable logs and other services
	sudo update-rc.d rsyslog disable
	sudo update-rc.d triggerhappy disable

	sudo /etc/init.d/rsyslog stop | true
	sudo /etc/init.d/rsyslog stop
	sudo /etc/init.d/triggerhappy stop | true
	sudo /etc/init.d/triggerhappy stop

	sudo rm -rf /var/log/*
	sudo rm -rf /home/pi/

	sudo aptitude purge wolfram-engine sonic-pi pistore minecraft-pi -y

	#//Update & Upgrade
	#sudo aptitude purge desktop-base lightdm lxappearance lxde-common lxde-icon-theme \
	#lxinput lxpanel lxpolkit lxrandr lxsession-edit lxshortcut lxtask lxterminal squeak-vm \
	#pistore scratch lxde-core lxde nuscratch raspberrypi-net-mods raspberrypi-ui-mods -y

	#sudo aptitude purge oracle-java7-jdk wolfram-engine omxplayer zenity midori libenchant1c2a \
	#libwebkitgtk-1.0-0 aspell aspell-en cifs-utils gnome-icon-theme gnome-themes-standard-data -y

	#sudo apt-get remove x11-common midori lxde python3 python3-minimal python-picamera xdg-utils -y

	#sudo apt-get autoremove -y

	#sudo apt-get remove `sudo dpkg --get-selections | grep "\-dev" | sed s/install//` -y
	#sudo apt-get remove `sudo dpkg --get-selections | grep -v "deinstall" | grep x11 | sed s/install//` -y
	#sudo apt-get remove `sudo dpkg --get-selections | grep -v "deinstall" | grep sound | sed s/install//` -y

	#sudo apt-get remove gcc-4.4-base:armhf gcc-4.5-base:armhf gcc-4.6-base:armhf gcc-4.7-base:armhf -y
	sudo apt-get autoremove -y

	#sudo apt-mark hold raspberrypi-bootloader
	#sudo apt-get update -y
	#sudo apt-get upgrade -y

	sudo apt-get clean -y

	sudo dpkg-reconfigure tzdata

	@echo
	@echo 'Reboot the System Manually'

2: #// Install Software

	sudo aptitude install git vim zsh autojump tmux screen htop ntp ntpdate fbi python-dev python-rpi.gpio \
	python-smbus i2c-tools bluez bluez-tools python-gobject python-gobject-2 snmp libsnmp-python python-pysnmp4 \
	python-pysnmp-common python-pip batctl bridge-utils iw wireless-tools iperf mysql-client mysql-server \
	python-mysqldb -y

	sudo pip install flask
	sudo pip install flask-wtf
	sudo pip install Flask-Cache
	sudo pip install flask-compress
	sudo pip install Flask-Login
	sudo pip install tornado

	#pip install flask-login
	#pip install flask-openid
	#pip install sqlalchemy



	#@echo 'Mosqitto'
	#sudo aptitude install python-mosquitto -y

	sudo apt-get clean -y

	@echo "Optimizing MySQL"
	sudo cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak
	sudo cp conf/my.cnf /etc/mysql/my.cnf
	sudo service mysql restart
	@echo

4: #// Install Addicional Gateway Software

	#// Mosquitto Server
	cd /tmp/; wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key; sudo apt-key add mosquitto-repo.gpg.key
	cd /etc/apt/sources.list.d/; sudo wget http://repo.mosquitto.org/debian/mosquitto-stable.list
	sudo aptitude update -y
	sudo aptitude install mosquitto -y
	@echo

5:	#// Configuration Variables

	#//Set git Variables
	git config --global user.email ABalanuta@users.noreply.github.com
	git config --global user.name ABalanuta

	#// remove backlight timeout
	sudo sed -i 's/BLANK_TIME=30/BLANK_TIME=0/' /etc/kbd/config

	#// add event rule
	#sudo cp conf/95-stmpe.rules /etc/udev/rules.d/95-stmpe.rules

	#// touchscreen calibration values
	#sudo mkdir /etc/X11/xorg.conf.d; true
	#sudo cp conf/99-calibration.conf /etc/X11/xorg.conf.d/

	#//bugfix X would not start wthout it
	#sudo sed -i 's/fb0/fb1/' /usr/share/X11/xorg.conf.d/99-fbturbo.conf


	#// Auto Load Modules
	#sudo cp conf/modules /etc/modules

	#// Remove Blacklist of I2C and spi
	#sudo sed -i 's/blacklist\ i2c-bcm2708/#blacklist\ i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
	#sudo sed -i 's/blacklist\ spi-bcm2708/#blacklist\ spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf

	#// Startup Script
	sudo cp conf/StartUP /etc/init.d/StartUP
	cd /etc/init.d/; sudo chmod +x StartUP
	sudo update-rc.d StartUP remove; true
	sudo update-rc.d StartUP defaults; true
	@echo

	#//Aux Scripts
	sudo mkdir /opt/peromas -p; true
	sudo cp conf/start_batman.py /opt/peromas/
	sudo cp conf/update_motd.sh /opt/peromas/
	sudo cp conf/startup.png /opt/peromas/

	#// Ajust TimeZone
	sudo dpkg-reconfigure tzdata

	#// NTP
	sudo cp conf/crontab /etc/crontab
	sudo /etc/init.d/cron restart

	#sudo python conf/change_host.py

	@echo 'Reboot the System Manually'

6: #// Test touchscreen

	@echo 'Test Soft'
	sudo apt-get install evtest tslib libts-bin -y
	sudo apt-get clean -y
	@echo

	#// Touchscreen
	sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate
	sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_test


	#dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait


	@echo
	@echo 'Option 6 DONE'
	@echo

7: #// Test X

	FRAMEBUFFER=/dev/fb1 startx

8: #// Backup MySQL
	sudo mysqldump -uroot -p3O7DCWP2HLR01471G9PZQ6U7X PeromasDB > /tmp/PeromasDB.sql
	scp /tmp/PeromasDB.sql ist168206@sigma.ist.utl.pt:~
	scp /tmp/PeromasDB.sql ist168206@sigma.ist.utl.pt:~/PeromasDB.sql_$(shell date +%d-%m-%y_%Hh%Mm)_$(shell hostname)

9: #// Restore MySQL
	scp ist168206@sigma.ist.utl.pt:~/PeromasDB.sql /tmp/PeromasDB.sql
	sudo mysql-uroot -p3O7DCWP2HLR01471G9PZQ6U7X PeromasDB < /tmp/PeromasDB.sql

10: #// Update Nodes from git and restar APP
	ssh -A 172.20.126.2 "cd /home/artur-adm/git/thesisPI; git pull; sudo reboot"; true
	ssh -A 172.20.126.3 "cd /home/artur-adm/git/thesisPI; git pull; sudo reboot"; true
	ssh -A 172.20.126.4 "cd /home/artur-adm/git/thesisPI; git pull; sudo reboot"; true
	ssh -A 172.20.126.5 "cd /home/artur-adm/git/thesisPI; git pull; sudo reboot"; true
