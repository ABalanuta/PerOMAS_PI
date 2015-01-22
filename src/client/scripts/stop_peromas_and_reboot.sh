sudo tmux send -t main.0 C-c
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/blue.jpg
sleep 8
sudo killall python
sudo reboot&
sudo fbi -T 2 -d /dev/fb1 -noverbose -a /home/artur-adm/git/thesisPI/src/client/scripts/power.jpg
