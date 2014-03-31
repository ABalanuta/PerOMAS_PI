sudo modprobe batman-adv

sudo ifconfig wlan0 down
sudo ifconfig wlan0 mtu 1528

sudo iwconfig wlan0 ap 02:11:87:26:34:31
sudo iwconfig wlan0 mode ad-hoc essid BatmanNetwork
#sudo iwconfig eth0 ap any
sudo iwconfig wlan0 channel 1
sudo iwconfig wlan0 rate auto
#sudo iwconfig wlan0 enc off
sudo iwconfig wlan0 key off
sudo ifconfig wlan0 up

sudo batctl if add wlan0
