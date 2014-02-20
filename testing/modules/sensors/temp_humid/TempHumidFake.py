#!/usr/bin/python
from random import randint
from time import sleep
from threading import Thread
from datetime import datetime



class TempHumidFake(Thread):

    def __init__(self, hub):
        self.stopped = False
        Thread.__init__(self)
        self.hub = hub
        self.started = datetime.now()
        self.last_update = datetime.now()
        self.temp = 0
        self.humid = 0
        self.update()	# Runs one time

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.update()

    def update(self):
		self.humid = randint(20, 100)
		self.temp = randint(20, 35)
		self.lastUpdate = datetime.now()
		sleep(1.5)
        
    def runtime(self):
        return str(self.lastUpdate-self.started).split(".")[0]

#Runs only if called
if __name__ == "__main__":

    started = datetime.now()

    print "#TEST#"
    print "#Starting#"
    d = TempHumidFake()
    d.start()

    while True:
        print "Runtime:", d.runtime(), "\tTemp:", d.temp, "\tHumid:", d.humid
        sleep(2)

    d.stop()
    print "#Sttoped#\n\n"
