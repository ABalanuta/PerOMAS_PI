#!/usr/bin/env python
"""PITFT interface made using the pygame lib"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import sys
import platform
import pygame
import pygbutton
from time import sleep
from threading import Thread
from pygame.locals import *


class TFT(Thread):

    FPS             = 20
    WINDOWWIDTH     = 320
    WINDOWHEIGHT    = 240
    size            = (WINDOWWIDTH, WINDOWHEIGHT)

    WHITE           = (255, 255, 255)
    BLACK           = (  0,   0,   0)

    BTN_BULB_ON     = 'images/light_bulb_on_80.png'
    BTN_BULB_OFF    = 'images/light_bulb_off_80.png'
    BTN_FORWARD     = 'images/forward_60.png'
    BTN_BACK        = 'images/back_60.png'

    myfont_18       = pygame.font.SysFont("monospace", 18)
    myfont_22       = pygame.font.SysFont("monospace", 22)
    myfont_30       = pygame.font.SysFont("monospace", 30)
        
    DASH_LABEL      = myfont_22.render("Dash", 1, WHITE)
    LUZES_LABEL     = myfont_30.render("Luzes", 1, WHITE)
    AC_LABEL        = myfont_30.render("AC", 1, WHITE)
    AUX_LABEL       = myfont_30.render("Info", 1, WHITE)

    TEMPERATURE_LABEL   = myfont_18.render(u"Temperature = 25 C", 1, WHITE)
    HUMIDITY_LABEL      = myfont_18.render(u"Humidity = 25.1 %", 1, WHITE)
    LUMINOSITY_LABEL    = myfont_18.render(u"Luminosity = 200 Lux", 1, WHITE)
    POWER_LABEL         = myfont_18.render(u"Power = 207 Watts", 1, WHITE)


    button_forward  = pygbutton.PygButton((WINDOWWIDTH-60,  WINDOWHEIGHT-60, 60, 60), normal=BTN_FORWARD)
    button_back     = pygbutton.PygButton((0,  WINDOWHEIGHT-60, 60, 60), normal=BTN_BACK)

    button_light_1  = pygbutton.PygButton((WINDOWWIDTH/2-90,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)
    button_light_2  = pygbutton.PygButton((WINDOWWIDTH/2+30,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)


    button_light_1_s    = True
    button_light_2_s    = False

    init_menu   = 0
    n_menus     = 3

    def __init__(self, hub):
        Thread.__init__(self)
        self.hub = hub

        # for Adafruit PiTFT:
        if 'armv6l' in platform.uname():
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

    def stop(self):
        self.stopped = True
        sleep(0.1)
        pygame.quit()

    def run(self):
        self.stopped = False

        # Init pygame and screen
        pygame.display.init()
        pygame.font.init()
        if 'armv6l' in platform.uname():
            pygame.mouse.set_visible(False)
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])

        while not self.stopped:
            self.update()

    def update(self):
        self.screen.fill(self.BLACK)
        self.menu()
        pygame.display.update()
        self.FPSCLOCK.tick(self.FPS)
        self.handleEvents()

    def handleEvents(self):

        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.stop()


            events = self.button_forward.handleEvent(event)
            if 'click' in events:
                self.init_menu = (self.init_menu+1)%self.n_menus

            events = self.button_back.handleEvent(event)
            if 'click' in events:
                self.init_menu = (self.init_menu-1)%self.n_menus



            events = self.button_light_1.handleEvent(event)
            if 'click' in events:
                if self.button_light_1_s:
                    self.button_light_1.setSurfaces(self.BTN_BULB_OFF)
                    self.button_light_1_s = False
                else:
                    self.button_light_1.setSurfaces(self.BTN_BULB_ON)
                    self.button_light_1_s = True

            events = self.button_light_2.handleEvent(event)
            if 'click' in events:
                if self.button_light_2_s:
                    self.button_light_2.setSurfaces(self.BTN_BULB_OFF)
                    self.button_light_2_s = False
                else:
                    self.button_light_2.setSurfaces(self.BTN_BULB_ON)
                    self.button_light_2_s = True

    def menu(self):

        self.button_forward.draw(self.screen)
        self.button_back.draw(self.screen)

        if self.init_menu == 0:
            self.screen.blit(self.LUZES_LABEL , (self.WINDOWWIDTH/2-self.LUZES_LABEL.get_width()/2, 2))

            self.button_light_1.draw(self.screen)
            self.button_light_2.draw(self.screen)

        elif self.init_menu == 1:
            self.screen.blit(self.AC_LABEL , (self.WINDOWWIDTH/2-self.AC_LABEL.get_width()/2, 2))
            #self.screen.blit(TEMPERATURE_LABEL , (50, 32))
            #self.screen.blit(HUMIDITY_LABEL ,    (50, 62))
            #self.screen.blit(LUMINOSITY_LABEL ,  (50, 92))
            #self.screen.blit(POWER_LABEL ,       (50, 122))
        
        elif self.init_menu == 2:
            self.screen.blit(self.AUX_LABEL , (self.WINDOWWIDTH/2-self.AUX_LABEL.get_width()/2, 2))


if __name__ == '__main__':

    print "#TEST#"
    print "#Starting#"
    t = TFT(None)
    t.start()
    try:
        while True:
            sleep(1)
    except: 
        t.stop()
    print "#Sttoped#\n\n"
