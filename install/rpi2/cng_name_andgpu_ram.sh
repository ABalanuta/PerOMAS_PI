#change the hostname 
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
NEW_HOSTNAME="Pi"
sudo sed -i "s/$CURRENT_HOSTNAME/$NEW_HOSTNAME/g" /etc/hostname
sudo sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts

## get current memory split from /boot/config.txt
CUR_GPU_MEM=`cat /boot/config.txt  | grep gpu_mem`
if [ -z "$CUR_GPU_MEM" ]
then
	echo "#GPU MEM SPLIT"  | sudo tee -a /boot/config.txt
	echo "gpu_mem=16" | sudo tee -a /boot/config.txt
fi
