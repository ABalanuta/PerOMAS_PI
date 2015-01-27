## get current memory split from /boot/config.txt
TFT=`cat  /boot/cmdline.txt | grep fbtft_device`
if [ -z "$TFT" ]
then
	echo "dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait fbcon=map:10 fbtft_device.name=pitft fbtft_device.rotate=90 fbtft_device.speed=32000000 fbtft_device.fps=30 fbtft_device.debug=0 fbtft_device.verbose=0" | sudo tee /boot/cmdline.txt
fi