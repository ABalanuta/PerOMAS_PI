all: install

install:
	sudo python change_host.py
	sudo cp StartUP /etc/init.d/StartUP
	sudo cp send_Email_With_IP.py /opt/send_Email_With_IP.py
	cd /etc/init.d/
	sudo chmod +x StartUP
	sudo update-rc.d StartUP defaults
