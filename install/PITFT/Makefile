all: update

update:
	sudo apt-get update -y
	sudo apt-get install evtest tslib libts-bin -y
	@echo "make 1 #then reboot"
	@echo "make 2 #after reboot"

1:
	@echo "Installing..."
	sudo dpkg -i -B *.deb

	@echo "Configuring..."
	sudo rm /usr/share/X11/xorg.conf.d/99-fbturbo.conf; \
	sudo cp modules /etc/modules;
	sudo cp adafruit.conf /etc/modprobe.d/adafruit.conf;
	sudo mkdir /etc/X11/xorg.conf.d; \
	sudo cp 99-calibration.conf /etc/X11/xorg.conf.d/99-calibration.conf;
	sudo cp 95-stmpe.rules /etc/udev/rules.d/95-stmpe.rules;
	
	@echo "Rebooting..."	
	sudo reboot
2:
	
