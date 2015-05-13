thesisPI
========

#### Instalation based on the RASPBIAN (Debian Wheezy) image from :
	## Version:January 2014
	## Release date:2014-01-07
	## Default login:pi / raspberry
	## URL:raspbian.org
	## http://www.raspberrypi.org/forums/viewtopic.php?f=66&t=57783

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
	ssh artur-adm@ IP
	
	mkdir .ssh; cd .ssh
	touch authorized_keys; chmod 600 authorized_keys
	echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDqSdbG54NtIdcUlNmp2erNWZdDtKu4aa5H5qGVlHMq560BjlKQEHnPKsjzgqFIOrgJj0xZLmyDDoDAeEfTn7DaArqwjIRTJKmiwZ7u4XsqzoChIkEFDyQCIt009S+GLDSibM8gwej3s1MqAhaosaWukCkEoeXqh5AuP20JwkSlT7HEoxyk00NsG/q/WlG9jR+TRQv8rm5Ca9LiVjzufMqBbZEsBiYiTkjRAXY3h1WANP+dBucXfZUprrlZUgbb8lKqQL3CbKOI2MSAkSRxZD02AGXRZdZdhStM+DNR4aFvsgnkYacgTSzIbK6XGrHNp5zdnv6iBHtTJW+6i9ESHya+WZEVvs94t4J5vlOV7v5pKNYWU07SS9vTGog8LxbJjJY2I2/4nTeJUvhx+KxlKRWexKi5D0U5jWnkycEqIKwihREZ95HYC0iE+MjZjc+8lvyasFHNNV9uyLpHGyZiebEawtPXl1M0tPj6qdX+mr/KrpEcZzCYcFuLhXwxr65Fdi14jrIGiL29fbe9GsTGM0r34zz7McmqejP5yD0EKaiwU54hDMdNBy3mTckfNJDR25ZUBh1x5frmzct+hsuu+5S1Xzs484vjgtp6IJcKcLDJARyo3yqjFHlZFKqqLiwe47xjI1jBRene/Qq2Hya0XzfwNbmsVr8nmq+/tttJliEbfw==" >> authorized_keys
	
	
	//Delete Default user
	sudo deluser pi
	
	//Clone the repo
	mkdir git; cd git
	git clone git@github.com:AliensGoo/thesisPI.git
	cd thesisPI
	git checkout dev
