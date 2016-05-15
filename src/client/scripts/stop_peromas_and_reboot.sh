sudo tmux send -t main.0 C-c
sleep 1
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/blue.jpg
sleep 5
sudo killall python
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/power.jpg
sleep 1
sudo reboot&
