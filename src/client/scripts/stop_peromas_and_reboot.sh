sudo tmux send -t main.0 C-c
#sleep 1
#sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/blue.jpg
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/power.jpg
sleep 15
sudo killall python
sleep 3
sudo reboot
