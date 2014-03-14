sudo modprobe batman-adv

sudo ifconfig wlan0 mtu 1528
sudo iwconfig wlan0 mode ad-hoc essid BatmanNetwork
sudo iwconfig wlan0 channel 1
sudo iwconfig wlan0 rate auto
sudo iwconfig wlan0 key 0123-4567-89
#sudo iwconfig wlan0 modu auto
sudo batctl if add wlan0
