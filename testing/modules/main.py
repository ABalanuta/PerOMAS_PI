#!/usr/bin/python

from sensors.temp_and_humid.sensTempHum import TermoHumid
from interaction.lcd.lcdmenu import *
import datetime


global thermo
global lcd

thermo = TermoHumid()
thermo.start()

sensorList = []
sensorList.append(thermo)


lcd = LCD(sensorList)
lcd.start()


#started = datetime.now()
