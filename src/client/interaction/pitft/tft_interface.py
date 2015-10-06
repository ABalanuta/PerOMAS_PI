#!/usr/bin/env python
"""PITFT interface made using the pygame lib"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import platform
import pygame
import pygbutton
import subprocess
from time import sleep
from threading import Thread
from datetime import datetime, timedelta
from pygame.locals import *


class TFT(Thread):

    DEBUG           = False

    FPS             = 10
    WINDOW_WIDTH    = 320
    WINDOW_HEIGHT   = 240
    WINDOW_SIZE     = (WINDOW_WIDTH, WINDOW_HEIGHT)

    WHITE           = (255, 255, 255)
    BLACK           = (  0,   0,   0)
    BLUE            = (  0,   0, 255)
    RED             = (255,   0,   0)
    YELLOW          = (255, 204,  51)
    LIGHT_BLUE      = ( 51, 204, 255)

    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))

    BTN_BULB_ON     = LOCAL_PATH + '/images/light_bulb_on_80.png'
    BTN_BULB_OFF    = LOCAL_PATH + '/images/light_bulb_off_80.png'
    BTN_FORWARD     = LOCAL_PATH + '/images/forward_60.png'
    BTN_BACK        = LOCAL_PATH + '/images/back_60.png'

    MYFONT_18       = pygame.font.SysFont("monospace", 18)
    MYFONT_22       = pygame.font.SysFont("monospace", 22)
    MYFONT_29       = pygame.font.SysFont("monospace", 29)
    MYFONT_32       = pygame.font.SysFont("monospace", 32)
    MYFONT_40       = pygame.font.SysFont("monospace", 40)
    MYFONT_50       = pygame.font.SysFont("monospace", 50)
    MYFONT_85       = pygame.font.SysFont("monospace", 85)
        
    DASH_LABEL      = MYFONT_22.render("Dash", 1, WHITE)
    LUZES_LABEL     = MYFONT_50.render("Luzes", 1, WHITE)
    AC_LABEL        = MYFONT_50.render("AC", 1, WHITE)
    AUX_LABEL       = MYFONT_50.render("Info", 1, WHITE)
    KEY_LABEL       = MYFONT_50.render("Api Key", 1, WHITE)

    TEMPERATURE_LABEL   = MYFONT_18.render(u"Temperature = 25 C", 1, WHITE)
    HUMIDITY_LABEL      = MYFONT_18.render(u"Humidity = 25.1 %", 1, WHITE)
    LUMINOSITY_LABEL    = MYFONT_18.render(u"Luminosity = 200 Lux", 1, WHITE)
    POWER_LABEL         = MYFONT_18.render(u"Power = 207 Watts", 1, WHITE)

    WHO_LABEL           = MYFONT_40.render(u"Who are you?", 1, WHITE)

    INIT_MENU           = 3
    MAX_MENU            = 5

    FEEDBACK_TIMEOUT    = 300 #Seconds

    #Buttons
    button_forward  = pygbutton.PygButton((WINDOW_WIDTH-60,  WINDOW_HEIGHT-60, 60, 60), normal=BTN_FORWARD)
    button_back     = pygbutton.PygButton((             0,  WINDOW_HEIGHT-60, 60, 60), normal=BTN_BACK)

    button_light_1  = pygbutton.PygButton((WINDOW_WIDTH/2-90,  WINDOW_HEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)
    button_light_2  = pygbutton.PygButton((WINDOW_WIDTH/2+30,  WINDOW_HEIGHT/2-45, 60, 60), normal=BTN_BULB_ON)

    button_minus_two    = pygbutton.PygButton(( 15, 80, 65, 65), "-3", font=MYFONT_50, bgcolor=BLUE)
    button_minus_one    = pygbutton.PygButton(( 90, 80, 65, 65), "-1", font=MYFONT_50, bgcolor=LIGHT_BLUE)
    button_plus_one     = pygbutton.PygButton((165, 80, 65, 65), "+1", font=MYFONT_50, bgcolor=YELLOW)
    button_plus_two     = pygbutton.PygButton((240, 80, 65, 65), "+3", font=MYFONT_50, bgcolor=RED)

    button_user_1       = pygbutton.PygButton((  0,  60, 160, 60), "User 1", font=MYFONT_32)
    button_user_2       = pygbutton.PygButton((160,  60, 160, 60), "User 2", font=MYFONT_32)
    button_user_3       = pygbutton.PygButton((  0, 120, 160, 60), "User 3", font=MYFONT_32)
    button_user_4       = pygbutton.PygButton((160, 120, 160, 60), "User 4", font=MYFONT_32)

    button_user_l       = pygbutton.PygButton((  0, 180, 160, 60), "<",      font=MYFONT_50, bgcolor=YELLOW)
    button_user_r       = pygbutton.PygButton((160, 180, 160, 60), ">",      font=MYFONT_50, bgcolor=YELLOW)
    button_user_cancel  = pygbutton.PygButton((160, 180, 160, 60), "Cancel", font=MYFONT_40, bgcolor=RED)

    def __init__(self, hub):
        Thread.__init__(self)
        self.hub = hub
        self.relay = None
        self.last_feedback_set = datetime.now() - timedelta(1)
        self.feedback_value = 0
        self.feedback_user_page = 0
        self.feedback_user_array = list()
        self.ip = "0.0.0.0"

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
            while not set(self.hub.keys()).issuperset(
                set(["RELAY", "TEMPERATURE", "HUMIDITY", "LUMINOSITY", "CURRENT", "USER MANAGER", "BLUETOOTH"])):
                if self.DEBUG:
                    print "PITFT waiting for the Modules to be Loaded"
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
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
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
                    self.INIT_MENU = (self.INIT_MENU+1)%self.MAX_MENU
                    to_draw = True

                events = self.button_back.handleEvent(event)
                if 'click' in events:
                    self.INIT_MENU = (self.INIT_MENU-1)%self.MAX_MENU
                    to_draw = True

                

                if self.INIT_MENU == 0:

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


                if self.INIT_MENU == 1:

                    events = self.button_minus_two.handleEvent(event)
                    if 'click' in events:
                        self.feedback_value = -3
                        self.INIT_MENU = 1.1
                        to_draw = True

                    events = self.button_minus_one.handleEvent(event)
                    if 'click' in events:
                        self.feedback_value = -1
                        self.INIT_MENU = 1.1
                        to_draw = True

                    events = self.button_plus_one.handleEvent(event)
                    if 'click' in events:
                        self.feedback_value = 1
                        self.INIT_MENU = 1.1
                        to_draw = True

                    events = self.button_plus_two.handleEvent(event)
                    if 'click' in events:
                        self.feedback_value = 3
                        self.INIT_MENU = 1.1
                        to_draw = True


                if self.INIT_MENU == 1.1:

                    events = self.button_user_l.handleEvent(event)
                    if 'click' in events:
                        self.feedback_user_page -= 1
                        to_draw = True

                    events = self.button_user_r.handleEvent(event)
                    if 'click' in events:
                        self.feedback_user_page += 1
                        to_draw = True

                    events = self.button_user_cancel.handleEvent(event)
                    if 'click' in events:
                        self.INIT_MENU = 1
                        self.feedback_user_page = 0
                        to_draw = True

                    events = self.button_user_1.handleEvent(event)
                    if 'click' in events:
                        usr = self.feedback_user_array[0]
                        usr_obj = self.hub["USER MANAGER"].getUser(usr)
                        new_setpoint = usr_obj.setpoint + self.feedback_value
                        usr_obj.set_setpoint(new_setpoint)
                        self.last_feedback_set = datetime.now()
                        self.INIT_MENU = 1
                        to_draw = True

                    events = self.button_user_2.handleEvent(event)
                    if 'click' in events:
                        usr = self.feedback_user_array[1]
                        usr_obj = self.hub["USER MANAGER"].getUser(usr)
                        new_setpoint = usr_obj.setpoint + self.feedback_value
                        usr_obj.set_setpoint(new_setpoint)
                        self.last_feedback_set = datetime.now()
                        self.INIT_MENU = 1
                        to_draw = True
                    
                    events = self.button_user_3.handleEvent(event)
                    if 'click' in events:
                        usr = self.feedback_user_array[2]
                        usr_obj = self.hub["USER MANAGER"].getUser(usr)
                        new_setpoint = usr_obj.setpoint + self.feedback_value
                        usr_obj.set_setpoint(new_setpoint)
                        self.last_feedback_set = datetime.now()
                        self.INIT_MENU = 1
                        to_draw = True
                    
                    events = self.button_user_4.handleEvent(event)
                    if 'click' in events:
                        usr = self.feedback_user_array[3]
                        usr_obj = self.hub["USER MANAGER"].getUser(usr)
                        new_setpoint = usr_obj.setpoint + self.feedback_value
                        usr_obj.set_setpoint(new_setpoint)
                        self.last_feedback_set = datetime.now()
                        self.INIT_MENU = 1
                        to_draw = True

            if to_draw:
                self.draw()
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

        self.button_user_1._propSetVisible(False)
        self.button_user_2._propSetVisible(False)
        self.button_user_3._propSetVisible(False)
        self.button_user_4._propSetVisible(False)

        self.button_user_l._propSetVisible(False)
        self.button_user_r._propSetVisible(False)
        self.button_user_cancel._propSetVisible(False)


        if self.INIT_MENU == 0:
            self.button_forward._propSetVisible(True)
            self.button_forward.draw(self.screen)

            self.screen.blit(self.LUZES_LABEL , (self.WINDOW_WIDTH/2-self.LUZES_LABEL.get_width()/2, 2))

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

        elif self.INIT_MENU == 1:

            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)

            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)
            self.screen.blit(self.AC_LABEL , (self.WINDOW_WIDTH/2-self.AC_LABEL.get_width()/2, 2))
            
            # Limits the number of feedbacks
            if  (datetime.now()-self.last_feedback_set).total_seconds() > self.FEEDBACK_TIMEOUT:
            
                self.button_minus_two._propSetVisible(True)
                self.button_minus_one._propSetVisible(True)
                self.button_plus_one._propSetVisible(True)
                self.button_plus_two._propSetVisible(True)

                self.button_minus_two.draw(self.screen)
                self.button_minus_one.draw(self.screen)
                self.button_plus_one.draw(self.screen)
                self.button_plus_two.draw(self.screen)
            else:
                t = self.FEEDBACK_TIMEOUT-((datetime.now()-self.last_feedback_set).total_seconds())
                l1 = self.MYFONT_50.render("Wait", 1, self.WHITE)
                l2 = self.MYFONT_50.render(str(int(t)), 1, self.WHITE)
                l3 = self.MYFONT_50.render("seconds", 1, self.WHITE)
                self.screen.blit(l1, (self.WINDOW_WIDTH/2-l1.get_width()/2, 50))
                self.screen.blit(l2, (self.WINDOW_WIDTH/2-l2.get_width()/2, 100))
                self.screen.blit(l3, (self.WINDOW_WIDTH/2-l3.get_width()/2, 150))
       
        elif self.INIT_MENU == 1.1:

            self.screen.blit(self.WHO_LABEL , (self.WINDOW_WIDTH/2-self.WHO_LABEL.get_width()/2, 2))

            present_users = self.hub["USER MANAGER"].getPresentUsers()
            present_users.sort()
            page_users = present_users

            #Selects only the users in actual page
            if len(page_users) > (self.feedback_user_page+1)*4:
                page_users = page_users[self.feedback_user_page*4:self.feedback_user_page*4+4]
            else:
                page_users = page_users[self.feedback_user_page*4:]

            self.feedback_user_array = page_users

            spaces = [self.button_user_1, self.button_user_2, self.button_user_3, self.button_user_4]

            for i in range(0, len(page_users)):
                button = spaces[i]
                username = page_users[i]
                button._caption = username
                button._update()
                button._propSetVisible(True)
                button.draw(self.screen)

            if self.feedback_user_page > 0:
               self.button_user_l._propSetVisible(True)
               self.button_user_l.draw(self.screen)

            if len(present_users) > (self.feedback_user_page+1)*4:
                self.button_user_r._propSetVisible(True) 
                self.button_user_r.draw(self.screen)

            if (self.feedback_user_page+1)*4 >= len(present_users):
                self.button_user_cancel._propSetVisible(True)
                self.button_user_cancel.draw(self.screen)

        #  I MENU
        elif self.INIT_MENU == 2:
            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)
            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)
            self.screen.blit(self.AUX_LABEL , (self.WINDOW_WIDTH/2-self.AUX_LABEL.get_width()/2, 2))

            temp  = round(self.hub["TEMPERATURE"].getTemperature(), 1)
            humid = round(self.hub["HUMIDITY"].getHumidity(), 1)
            lumi  = self.hub["LUMINOSITY"].getValue()
            curt  = round(self.hub["CURRENT"].getValue(), 1)

            t_label = self.MYFONT_22.render("Temperature  = "+str(temp)+"C"+chr(176), 1, self.WHITE)
            h_label = self.MYFONT_22.render("Humidity = "+str(humid)+" %", 1, self.WHITE)
            l_label = self.MYFONT_22.render("Luminosity = "+str(lumi)+" Lux", 1, self.WHITE)
            c_label = self.MYFONT_18.render("Consumption = "+str(curt)+" Watts", 1, self.WHITE)

            self.screen.blit(t_label , (30, 60))
            self.screen.blit(h_label , (30, 90))
            self.screen.blit(l_label , (30, 120))
            self.screen.blit(c_label , (30, 150))
        
        # BIG Temperatur MENU
        elif self.INIT_MENU == 3:
            self.button_forward._propSetVisible(True)
            self.button_back._propSetVisible(True)
            self.button_forward.draw(self.screen)
            self.button_back.draw(self.screen)

            temp  = round(self.hub["TEMPERATURE"].getTemperature(), 1)
            t_label = self.MYFONT_85.render(str(temp)+"C"+chr(176), 1, self.WHITE)
            self.screen.blit(t_label , (10, 60))


            #self.screen.blit(self.AC_LABEL , (self.WINDOW_WIDTH/2-self.AC_LABEL.get_width()/2, 2))

        # API key MENU
        elif self.INIT_MENU == 4:
            self.button_back._propSetVisible(True)
            self.button_back.draw(self.screen)

            self.screen.blit(self.KEY_LABEL , (self.WINDOW_WIDTH/2-self.KEY_LABEL.get_width()/2, 2))

            key = self.hub["API KEY"]
            k_label = self.MYFONT_85.render(key, 1, self.WHITE)
            ip_label = self.MYFONT_29.render(self.get_local_IP()+":5000", 1, self.WHITE)
            self.screen.blit(ip_label , (10, 65))
            self.screen.blit(k_label , (10, 100))


    def get_local_IP(self):

            try:
                p = subprocess.Popen("sudo ifconfig br0; sudo ifconfig bat0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                lines = p.stdout.readlines()
                for line in lines:
                    if "inet addr:" in line:
                        return str(line.split()[1].split(':')[1])
            except:
                return "0.0.0.0"

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
