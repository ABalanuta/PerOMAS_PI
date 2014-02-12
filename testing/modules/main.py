from sensors.temp_and_humid.sensTempHum import TermoHumid
from interaction.lcd.lcdmenu.py import *




global th

th = TermoHumid()

th.start()
print th.temp
th.stop()