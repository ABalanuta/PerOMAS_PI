thesisPI
========

#### Instalation based on the RASPBIAN (Debian Wheezy) image from :
	## Version:January 2014
	## Release date:2014-01-07
	## Default login:pi / raspberry
	## URL:raspbian.org
	## http://www.raspberrypi.org/downloads/

#### Before Instalation
	//Add new USer
	ssh pi@piX
	pass:raspberry
	sudo su
	adduser artur-adm
	pass:xxxxx
	sudo sed -i 's/pi/artur-adm/' /etc/sudoers
	exit
	
	//Copy SSH Key
	ssh-copy-id artur-adm@piX
	ssh artur-adm@piX
	
	//Delete Default user
	sudo deluser pi
