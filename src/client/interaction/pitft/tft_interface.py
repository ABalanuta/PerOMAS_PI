#!/usr/bin/env python
"""PITFT interface made using the pygame lib"""

__author__ = "Artur Balanuta"
__version__ = "1.0.3"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import platform
import pygame
import pygbutton
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime, timedelta
from page import PageManager
from pygame.locals import *

class TFT(Thread):

    DEBUG           = False

    FPS             = 10
    WINDOW_WIDTH    = 320
    WINDOW_HEIGHT   = 240
    WINDOW_SIZE     = (WINDOW_WIDTH, WINDOW_HEIGHT)
    BLACK           = (  0,   0,   0)

    def __init__(self, hub):
        Thread.__init__(self)
        self.hub = hub
        self.pageManager = PageManager(self)

        # for Adafruit PiTFT:
        if 'armv6l' in platform.uname():
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

        # Init pygame and screen
        pygame.display.init()
        pygame.font.init()
        if 'armv6l' in platform.uname():
            pygame.mouse.set_visible(False)
        self.logic = None

    def stop(self):
        self.stopped = True
        sleep(0.2)
        pygame.quit()

    def run(self):
        self.stopped = False
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        #wait for the ralay to load
        if 'armv6l' in platform.uname():
            dependencies = set(["RELAY", "TEMPERATURE", "HUMIDITY", "LUMINOSITY", "CURRENT","USER MANAGER",
                "SCHEDULE MANAGER", "LOGIC ENGINE"])
            waiting = len(dependencies)
            while waiting > 0:
                waiting = 0
                for x in dependencies:
                    if x not in self.hub:
                        waiting = waiting + 1
                        print "Waiting for ", x
                if self.DEBUG and waiting > 0:
                    print "PITFT waiting for "+str(waiting)+" Modules to be Loaded"
                sleep(0.5)

            self.relay = self.hub["RELAY"]
            self.scheduler = self.hub["SCHEDULE MANAGER"]
            self.logic = self.hub["LOGIC ENGINE"]
        self.draw()
        intermediate_update = 0

        while not self.stopped:
            self.update()
            if intermediate_update > self.FPS*5:
                self.draw()
                intermediate_update = 0
            else:
                intermediate_update += 1

    def update(self):
        self.FPSCLOCK.tick(self.FPS)
        self.handleEvents()

    def draw(self):
        if self.DEBUG:
            print "Draw Screen"
        self.screen.fill(self.BLACK)
        self.pageManager.render()
        pygame.display.update()

    def handleEvents(self):

        if self.stopped:
            return

        try:
            pevents = pygame.event.get()
        except:
            return

        for event in pevents:
                if self.DEBUG:
                    print event

                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.stop()

                redraw = self.pageManager.currentPage.handleEvent(event)
                if redraw and not self.stopped:
                    self.draw()
        return

    def get_local_IP(self):
        ip = "0.0.0.0"
        if 'armv6l' in platform.uname():
            try:
                p = subprocess.Popen("sudo ifconfig br0; sudo ifconfig bat0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                lines = p.stdout.readlines()
                for line in lines:
                    if "inet addr:" in line:
                        ip = str(line.split()[1].split(':')[1])
                        return ip
            except:
                return ip
        return ip

if __name__ == '__main__':

    print "#TEST#"
    print "#Starting#"
    t = TFT(None)
    t.start()
    try:
        while not t.stopped:
            sleep(0.2)
    except:
        t.stop()
    print "#Sttoped#\n\n"
