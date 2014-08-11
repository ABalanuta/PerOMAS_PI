#!/usr/bin/env python
"""PITFT interface made using the pygame lib"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import platform
import pygame
import pygbutton
from time import sleep
from threading import Thread
from pygame.locals import *


class TFT(Thread):

    DEBUG           = False

    FPS             = 10
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
    KEY_LABEL       = myfont_50.render("Api Key", 1, WHITE)

    TEMPERATURE_LABEL   = myfont_18.render(u"Temperature = 25 C", 1, WHITE)
    HUMIDITY_LABEL      = myfont_18.render(u"Humidity = 25.1 %", 1, WHITE)
    LUMINOSITY_LABEL    = myfont_18.render(u"Luminosity = 200 Lux", 1, WHITE)
    POWER_LABEL         = myfont_18.render(u"Power = 207 Watts", 1, WHITE)


    button_forward  = pygbutton.PygButton((WINDOWWIDTH-60,  WINDOWHEIGHT-60, 60, 60), normal=BTN_FORWARD)
    button_back     = pygbutton.PygButton((             0,  WINDOWHEIGHT-60, 60, 60), normal=BTN_BACK)

    button_light_1  = pygbutton.PygButton((WINDOWWIDTH/2-90,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)
    button_light_2  = pygbutton.PygButton((WINDOWWIDTH/2+30,  WINDOWHEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)

    button_minus_two  = pygbutton.PygButton(( 30,  100, 50, 50), "-2", bgcolor=(  0,   0, 255))
    button_minus_one  = pygbutton.PygButton((100,  100, 50, 50), "-1", bgcolor=( 51, 204, 255))
    button_plus_one   = pygbutton.PygButton((170,  100, 50, 50), "+1", bgcolor=(255, 204,  51))
    button_plus_two   = pygbutton.PygButton((240,  100, 50, 50), "+2", bgcolor=(255,   0,   0))

    init_menu   = 1
    n_menus     = 5

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
            
            # Init pygame and screen
            pygame.display.init()
            pygame.font.init()
            pygame.mouse.set_visible(False)

    def stop(self):
        self.stopped = True
        sleep(0.1)
        pygame.quit()

    def run(self):
        self.stopped = False

        #wait for the ralay to load
        if self.hub:
            while not set(self.hub.keys()).issuperset(set(["RELAY", "TEMPERATURE", "HUMIDITY", "LUMINOSITY", "CURRENT"])):
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

            while not "TEMPERATURE" in self.hub.keys():
                if self.DEBUG:
                    print "PITFT waiting for the Relay to be Loaded"
                    sleep(0.5)
        

        if 'armv6l' in platform.uname():    #Hides the cursor in running on the RPi
            pygame.mouse.set_visible(False)

        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, 0, 32)
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
        self.menu()
        pygame.display.update()

    def handleEvents(self):

        if self.stopped:
            return

        pevents = pygame.event.get()
        to_draw = False
        
        if pevents != None:
            for event in pevents: # event handling loop
    	    #print event

                if self.DEBUG:
                    print event

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

                events = self.button_minus_two.handleEvent(event)
                if 'click' in events:
                    print "-2"

                events = self.button_minus_one.handleEvent(event)
                if 'click' in events:
                    print "-1"

                events = self.button_plus_one.handleEvent(event)
                if 'click' in events:
                    print "+1"

                events = self.button_plus_two.handleEvent(event)
                if 'click' in events:
                    print "+2"

                events_x1 = self.button_light_1.handleEvent(event)
                if 'click' in events_x1:
                    sleep(0.1)
                    self.relay.flip_lights_x1()
                    to_draw = True

                events_x2 = self.button_light_2.handleEvent(event)
                if 'click' in events_x2:
                    sleep(0.1)
                    self.relay.flip_lights_x2()
                    to_draw = True

            if to_draw:
                self.draw()
                print "XPTO Draw sleep 1"
                sleep(0.7)

    def menu(self):

        
        self.button_light_1._propSetVisible(False)
        self.button_light_2._propSetVisible(False)
        self.button_forward._propSetVisible(False)
        self.button_back._propSetVisible(False)
        self.button_minus_two._propSetVisible(False)
        self.button_minus_one._propSetVisible(False)
        self.button_plus_one._propSetVisible(False)
        self.button_plus_two._propSetVisible(False)


        if self.init_menu == 0:

            self.button_forward._propSetVisible(True)
            self.button_forward.draw(self.screen)

            self.screen.blit(self.LUZES_LABEL , (self.WINDOWWIDTH/2-self.LUZES_LABEL.get_width()/2, 2))

            if self.relay.get_lights_x1_state():
                self.button_light_1.setSurfaces(self.BTN_BULB_ON)
            else:
                self.button_light_1.setSurfaces(self.BTN_BULB_OFF)

            if self.relay.get_lights_x2_state():
                self.button_light_2.setSurfaces(self.BTN_BULB_ON)
            else:
                self.button_light_2.setSurfaces(self.BTN_BULB_OFF)

            self.button_light_1._propSetVisible(True)
            self.button_light_2._propSetVisible(True)

            self.button_light_1.draw(self.screen)
            self.button_light_2.draw(self.screen)

        elif self.init_menu == 1:
            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)
            self.button_minus_two._propSetVisible(True)
            self.button_minus_one._propSetVisible(True)
            self.button_plus_one._propSetVisible(True)
            self.button_plus_two._propSetVisible(True)
            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)
            self.screen.blit(self.AC_LABEL , (self.WINDOWWIDTH/2-self.AC_LABEL.get_width()/2, 2))

            self.button_minus_two.draw(self.screen)
            self.button_minus_one.draw(self.screen)
            self.button_plus_one.draw(self.screen)
            self.button_plus_two.draw(self.screen)

        elif self.init_menu == 2:
            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)
            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)
            self.screen.blit(self.AUX_LABEL , (self.WINDOWWIDTH/2-self.AUX_LABEL.get_width()/2, 2))

            temp  = round(self.hub["TEMPERATURE"].getTemperature(), 1)
            humid = round(self.hub["HUMIDITY"].getHumidity(), 1)
            lumi  = self.hub["LUMINOSITY"].getValue()
            curt  = round(self.hub["CURRENT"].getValue(), 1)

            t_label = self.myfont_22.render("Temperature  = "+str(temp)+"C"+chr(176), 1, self.WHITE)
            h_label = self.myfont_22.render("Humidity = "+str(humid)+" %", 1, self.WHITE)
            l_label = self.myfont_22.render("Luminosity = "+str(lumi)+" Lux", 1, self.WHITE)
            #u_label = self.myfont_18.render(u"Luminosity = "+str(self.hub["LUMINOSITY"].getHumidity())+" Lux", 1, WHITE)
            c_label = self.myfont_18.render("Consumption = "+str(curt)+" Watts", 1, self.WHITE)

            self.screen.blit(t_label , (30, 60))
            self.screen.blit(h_label , (30, 90))
            self.screen.blit(l_label , (30, 120))
            self.screen.blit(c_label , (30, 150))
        
        elif self.init_menu == 3:
            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)
            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)
            

            temp  = round(self.hub["TEMPERATURE"].getTemperature(), 1)
            myfont_85 = pygame.font.SysFont("monospace", 85)
            t_label = myfont_85.render(str(temp)+"C"+chr(176), 1, self.WHITE)
            self.screen.blit(t_label , (10, 60))


            #self.screen.blit(self.AC_LABEL , (self.WINDOWWIDTH/2-self.AC_LABEL.get_width()/2, 2))

        elif self.init_menu == 4:
            self.button_back._propSetVisible(True)
            self.button_back.draw(self.screen)

            self.screen.blit(self.KEY_LABEL , (self.WINDOWWIDTH/2-self.KEY_LABEL.get_width()/2, 2))

            key  = self.hub["API KEY"]
            myfont_85 = pygame.font.SysFont("monospace", 85)
            k_label = myfont_85.render(key, 1, self.WHITE)
            self.screen.blit(k_label , (10, 60))

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
