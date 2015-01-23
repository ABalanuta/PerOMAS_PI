sudo tmux send -t main.0 C-c
sleep 4
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/blue.jpg
sleep 4
sudo killall python
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/power.jpg
sudo reboot&