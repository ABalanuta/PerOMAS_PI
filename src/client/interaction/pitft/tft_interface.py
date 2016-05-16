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
        self.ip = "0.0.0.0"
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
        pygame.mouse.set_visible(False)

        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)

    def stop(self):
        self.stopped = True
        sleep(0.2)
        pygame.quit()

    def run(self):
        self.stopped = False

        #wait for the ralay to load
        while self.hub and not set(self.hub.keys()).issuperset(
            set(["RELAY", "TEMPERATURE", "HUMIDITY", "LUMINOSITY", "CURRENT",
                "USER MANAGER", "BLUETOOTH", "SCHEDULE MANAGER", "LOGIC ENGINE"])):
            if self.DEBUG:
                print "PITFT waiting for the Modules to be Loaded"
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

        pevents = pygame.event.get()
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
            if 'armv6l' in platform.uname():
                try:
                    p = subprocess.Popen("sudo ifconfig br0; sudo ifconfig bat0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    lines = p.stdout.readlines()
                    for line in lines:
                        if "inet addr:" in line:
                            self.ip = str(line.split()[1].split(':')[1])
                            return self.ip
                except:
                    return self.ip
            return self.ip

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
