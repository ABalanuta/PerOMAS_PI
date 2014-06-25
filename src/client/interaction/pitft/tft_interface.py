#!/usr/bin/env python
"""PITFT interface made using the pygame lib"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
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

    DEBUG           = False

    FPS             = 15
    WINDOWWIDTH     = 320
    WINDOWHEIGHT    = 240
    size            = (WINDOWWIDTH, WINDOWHEIGHT)

    WHITE           = (255, 255, 255)
    BLACK           = (  0,   0,   0)

    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))

    BTN_BULB_ON     = LOCAL_PATH + '/images/light_bulb_on_80.png'
    BTN_BULB_OFF    = LOCAL_PATH + '/images/light_bulb_off_80.png'
    BTN_FORWARD     = LOCAL_PATH + '/images/forward_60.png'
    BTN_BACK        = LOCAL_PATH + '/images/back_60.png'

    myfont_18       = pygame.font.SysFont("monospace", 18)
    myfont_22       = pygame.font.SysFont("monospace", 22)
    myfont_50       = pygame.font.SysFont("monospace", 50)
        
    DASH_LABEL      = myfont_22.render("Dash", 1, WHITE)
    LUZES_LABEL     = myfont_50.render("Luzes", 1, WHITE)
    AC_LABEL        = myfont_50.render("AC", 1, WHITE)
    AUX_LABEL       = myfont_50.render("Info", 1, WHITE)

    TEMPERATURE_LABEL   = myfont_18.render(u"Temperature = 25 C", 1, WHITE)
    HUMIDITY_LABEL      = myfont_18.render(u"Humidity = 25.1 %", 1, WHITE)
    LUMINOSITY_LABEL    = myfont_18.render(u"Luminosity = 200 Lux", 1, WHITE)
    POWER_LABEL         = myfont_18.render(u"Power = 207 Watts", 1, WHITE)


    button_forward  = pygbutton.PygButton((WINDOWWIDTH-60,  WINDOWHEIGHT-60, 60, 60), normal=BTN_FORWARD)
    button_back     = pygbutton.PygButton((             0,  WINDOWHEIGHT-60, 60, 60), normal=BTN_BACK)

    button_light_1  = pygbutton.PygButton((WINDOWWIDTH/2-90,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)
    button_light_2  = pygbutton.PygButton((WINDOWWIDTH/2+30,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)

    init_menu   = 0
    n_menus     = 3

    def __init__(self, hub):
        Thread.__init__(self)
        self.hub = hub
        self.relay = None

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

        #wait for the ralay to load
        if self.hub:
            while not "RELAY" in self.hub.keys():
                if self.DEBUG:
                    print "PITFT waiting for the Relay to be Loaded"
                    sleep(0.5)
            self.relay = self.hub["RELAY"]
            l1_state = self.relay.get_lights_x1_state()
            l2_state = self.relay.get_lights_x2_state()

            if l1_state:
                self.button_light_1.setSurfaces(self.BTN_BULB_ON)
            else:
                self.button_light_1.setSurfaces(self.BTN_BULB_OFF)
            
            if l2_state:
                self.button_light_2.setSurfaces(self.BTN_BULB_ON)
            else:
                self.button_light_2.setSurfaces(self.BTN_BULB_OFF)

        # Init pygame and screen
        pygame.display.init()
        pygame.font.init()
        if 'armv6l' in platform.uname():
            pygame.mouse.set_visible(False)
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        #print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.draw()
        while not self.stopped:
            self.update()

    def update(self):
        #print "Update"
        self.FPSCLOCK.tick(self.FPS)
        self.handleEvents()

    def draw(self):
        if self.DEBUG:
            print "Draw Screen"
        self.screen.fill(self.BLACK)
        self.menu()
        pygame.display.update()

    def handleEvents(self):

        pevents = pygame.event.get()
        to_draw = False

        for event in pevents: # event handling loop
	    #print event

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.stop()


            events = self.button_forward.handleEvent(event)
            if 'click' in events:
                self.init_menu = (self.init_menu+1)%self.n_menus
                to_draw = True

            events = self.button_back.handleEvent(event)
            if 'click' in events:
                self.init_menu = (self.init_menu-1)%self.n_menus
                to_draw = True



            events = self.button_light_1.handleEvent(event)
            if 'click' in events:
                if self.relay.get_lights_x1_state():
                    self.button_light_1.setSurfaces(self.BTN_BULB_OFF)
                    self.relay.set_lights_x1_state(False)
                else:
                    self.button_light_1.setSurfaces(self.BTN_BULB_ON)
                    self.relay.set_lights_x1_state(True)
                to_draw = True

            events = self.button_light_2.handleEvent(event)
            if 'click' in events:
                if self.relay.get_lights_x2_state():
                    self.button_light_2.setSurfaces(self.BTN_BULB_OFF)
                    self.relay.set_lights_x2_state(False)
                else:
                    self.button_light_2.setSurfaces(self.BTN_BULB_ON)
                    self.relay.set_lights_x2_state(True)
                to_draw = True

        if to_draw:
            #print "XPTO Draw"
            self.draw()

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
