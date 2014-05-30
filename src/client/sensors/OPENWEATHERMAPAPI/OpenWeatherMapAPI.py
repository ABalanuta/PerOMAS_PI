#!/usr/bin/env python
"""Gets Temperature and Humidity values 
from api.openweathermap.org using the api key"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from urllib2 import urlopen
from json import loads as decode_json
from datetime import datetime

class OpenWeatherMapAPI():

    DEBUG       = False
    QUERY_PAGE  = "http://api.openweathermap.org/data/2.5/weather?q="
    LOCATION    = "Oeiras,PT"
    UNITS       = "metric"
    APPID       = "518039ab2b103e92a2ea6b66c97cf3bd"

    def __init__(self, hub):
        self.hub = hub
        self.last_update = datetime.now()
        self.humid = 0.0
        self.temp = 0
        self.updateValues()	# Runs one time

    def updateValues(self):
        resp = urlopen(self.QUERY_PAGE + self.LOCATION + "&units=" + self.UNITS + "&APPID=" + self.APPID)
        json = decode_json(resp.read())

        if "main" in json.keys():

            self.last_update = datetime.now()

            if "temp" in json["main"].keys():
                if self.DEBUG:
                    print "curr_Temp:", float(json["main"]["temp"]), "C"
                self.temp = float(json["main"]["temp"])

            if "humidity" in json["main"].keys():
                if self.DEBUG:
                    print "curr_Humidity:", int(json["main"]["humidity"]), "%"
                self.humid = int(json["main"]["humidity"])
            
        elif self.DEBUG:
            print "Error getting values from Server"
    
    def getTemperature(self):
        return self.temp

    def getHumidity(self):
        return self.humid

    def getLastUpdate(self):
        return str(self.last_update).split(".")[0].split()[1]

    def stop(self):
        return
        
#Runs only if called
if __name__ == "__main__":

    api = OpenWeatherMapAPI(None)
    print api.getTemperature()
    print api.getHumidity()
    print api.getLastUpdate()
