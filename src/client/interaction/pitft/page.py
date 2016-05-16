"""Page control and representation"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import platform
import pygame
import pygbutton
from time import sleep

class PageManager(object):

    def __init__(self, pallete):
        self.pallete = pallete
        p1 = LightsPage(pallete, self)
        p2 = TemperaturePage(pallete, self)
        p3 = KeyPage(pallete, self)

        p1.setNextPage(p2)
        p2.setPrevPage(p1)
        p2.setNextPage(p3)
        p3.setPrevPage(p2)

        self.currentPage = p1

    def next(self):
        self.currentPage.disableEvents()
        self.currentPage = self.currentPage.next

    def prev(self):
        self.currentPage.disableEvents()
        self.currentPage = self.currentPage.prev

    def setCurrentPage(self, page):
        self.currentPage.disableEvents()
        self.currentPage = page

    def render(self):
        self.currentPage.render()

class Page(object):

    DEVELOPMENT     = not 'armv6l' in platform.uname()
    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    BTN_FORWARD     = LOCAL_PATH + '/images/forward_60.png'
    BTN_BACK        = LOCAL_PATH + '/images/back_60.png'

    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        self.pallete = pallete
        self.manager = manager
        self.prev = prevPage
        self.next = nextPage
        self.WINDOW_WIDTH   = pallete.WINDOW_WIDTH
        self.WINDOW_HEIGHT  = pallete.WINDOW_HEIGHT
        BTN_H               = 60
        BTN_L               = 60
        self.button_back    = pygbutton.PygButton(
            (0, self.WINDOW_HEIGHT-BTN_H, BTN_L, BTN_H), normal=self.BTN_BACK)
        self.button_forward = pygbutton.PygButton(
            (self.WINDOW_WIDTH-BTN_L, self.WINDOW_HEIGHT-BTN_H,BTN_L, BTN_H), normal=self.BTN_FORWARD)
        self.disableEvents()

    def render(self):

        #Only render the signs if there are previous or next pages
        if  self.prev:
            self.button_back._propSetVisible(True)
            self.button_back.draw(self.pallete.screen)
        if self.next:
            self.button_forward._propSetVisible(True)
            self.button_forward.draw(self.pallete.screen)

    def disableEvents(self):
        self.button_back._propSetVisible(False)
        self.button_forward._propSetVisible(False)

    def setNextPage(self, page):
        self.next = page

    def setPrevPage(self, page):
        self.prev = page

    def handleEvent(self, event):

        events = self.button_back.handleEvent(event)
        if 'click' in events:
            self.manager.prev()
            return True

        events = self.button_forward.handleEvent(event)
        if 'click' in events:
            self.manager.next()
            return True

        return False

class LightsPage(Page):

    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    IMG_BULB_ON     = LOCAL_PATH + '/images/light_bulb_on.png'
    IMG_BULB_OFF    = LOCAL_PATH + '/images/light_bulb_off.png'
    IMG_EXIT        = LOCAL_PATH + '/images/exit_50.png'


    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
        BTN_H           = 128
        BTN_L           = 128
        BTN_E_H         = 50
        BTN_E_L         = 50

        BTN1_X          = ((self.WINDOW_WIDTH/2)-BTN_L)/2
        BTN1_Y          = (self.WINDOW_HEIGHT-BTN_H-60)/2
        BTN2_X          = ((self.WINDOW_WIDTH/2)-BTN_L)/2+self.WINDOW_WIDTH/2
        BTN2_Y          = (self.WINDOW_HEIGHT-BTN_H-60)/2
        BTN_E_X          = self.WINDOW_WIDTH/2 - BTN_E_L/2
        BTN_E_Y          = self.WINDOW_HEIGHT - BTN_E_H

        self.button_light_1 = pygbutton.PygButton((BTN1_X, BTN1_Y, BTN_H, BTN_L),normal=self.IMG_BULB_OFF)
        self.button_light_2 = pygbutton.PygButton((BTN2_X, BTN2_Y, BTN_H, BTN_L),normal=self.IMG_BULB_OFF)
        self.button_exit    = pygbutton.PygButton((BTN_E_X, BTN_E_Y, BTN_E_H, BTN_E_L),normal=self.IMG_EXIT)

        #Fake button states for DEBUG
        if self.DEVELOPMENT:
            self.x1 = False
            self.x2 = False

    def render(self):
        super(self.__class__,self).render()

        if not self.DEVELOPMENT:
            self.x1 = self.pallete.relay.get_lights_x1_state()
            self.x2 = self.pallete.relay.get_lights_x2_state()

        if self.x1:
            self.button_light_1.setSurfaces(self.IMG_BULB_ON)
        else:
            self.button_light_1.setSurfaces(self.IMG_BULB_OFF)

        if self.x2:
            self.button_light_2.setSurfaces(self.IMG_BULB_ON)
        else:
            self.button_light_2.setSurfaces(self.IMG_BULB_OFF)

        self.button_light_1.draw(self.pallete.screen)
        self.button_light_2.draw(self.pallete.screen)
        self.button_exit.draw(self.pallete.screen)

    #def disableEvents(self):
    #    super(self.__class__,self).disableEvents()
    #    self.button_light_1._propSetVisible(False)
    #    self.button_light_1._propSetVisible(False)

    def handleEvent(self, event):

        events = self.button_light_1.handleEvent(event)
        if 'click' in events:
            sleep(0.01)
            if not self.DEVELOPMENT:
                self.pallete.relay.flip_lights_x1()
            else:
                self.x1 = not self.x1
            return True

        events = self.button_light_2.handleEvent(event)
        if 'click' in events:
            sleep(0.01)
            if not self.DEVELOPMENT:
                self.pallete.relay.flip_lights_x2()
            else:
                self.x2 = not self.x2
            return True

        events = self.button_exit.handleEvent(event)
        if 'click' in events:
            sleep(0.01)
            if not self.DEVELOPMENT:
                self.pallete.relay.set_lights_x1_state(False)
                sleep(0.4)
                self.pallete.relay.set_lights_x2_state(False)
                sleep(0.1)
                self.pallete.logic.setACMode("Manual")
                self.pallete.relay.set_ac_speed(0)
            else:
                self.x1 = False
                self.x2 = False
            return True

        # return the response of the superclass
        return super(self.__class__,self).handleEvent(event)

class TemperaturePage(Page):

    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    COGWHEEL_BTN    = LOCAL_PATH + '/images/cogwheel_50.png'
    WHITE           = (255, 255, 255)
    MYFONT_85       = pygame.font.SysFont("monospace", 85)

    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
        self.AC_MENU    = Page(self.pallete, self.manager, prevPage=self)
        BTN_H           = 50
        BTN_L           = 50
        BTN1_X          = self.WINDOW_WIDTH/2 - BTN_L/2
        BTN1_Y          = self.WINDOW_HEIGHT - BTN_H

        self.button_cogwheel  = pygbutton.PygButton((BTN1_X, BTN1_Y, BTN_H, BTN_L),normal=self.COGWHEEL_BTN)

    def render(self):
        super(self.__class__,self).render()

        if not self.DEVELOPMENT:
            temp  = round(self.pallete.hub["TEMPERATURE"].getTemperature(), 1)
        else:
            temp = 20.1

        t_label = self.MYFONT_85.render(str(temp)+"C"+chr(176), 1, self.WHITE)
        self.pallete.screen.blit(t_label , (10, 60))
        self.button_cogwheel.draw(self.pallete.screen)

    def handleEvent(self, event):

        events = self.button_cogwheel.handleEvent(event)
        if 'click' in events:
            sleep(0.01)
            self.manager.setCurrentPage(self.AC_MENU)
            return True

        # return the response of the superclass
        return super(self.__class__,self).handleEvent(event)

class RebootPage(Page):

        LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
        IMG_REBOOT     = LOCAL_PATH + '/images/reboot_128.png'
        IMG_POWEROFF    = LOCAL_PATH + '/images/power_128.png'


        def __init__(self, pallete, manager, prevPage=None, nextPage=None):
            super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
            BTN_H           = 128
            BTN_L           = 128

            BTN1_X          = ((self.WINDOW_WIDTH/2)-BTN_L)/2
            BTN1_Y          = (self.WINDOW_HEIGHT-BTN_H-60)/2
            BTN2_X          = ((self.WINDOW_WIDTH/2)-BTN_L)/2+self.WINDOW_WIDTH/2
            BTN2_Y          = (self.WINDOW_HEIGHT-BTN_H-60)/2

            self.reboot = pygbutton.PygButton((BTN1_X, BTN1_Y, BTN_H, BTN_L),normal=self.IMG_REBOOT)
            self.poweroff = pygbutton.PygButton((BTN2_X, BTN2_Y, BTN_H, BTN_L),normal=self.IMG_POWEROFF)

        def render(self):
            super(self.__class__,self).render()
            self.reboot.draw(self.pallete.screen)
            self.poweroff.draw(self.pallete.screen)

        def handleEvent(self, event):

            events = self.reboot.handleEvent(event)
            if 'click' in events:
                sleep(0.01)
                if not self.DEVELOPMENT:
                    self.pallete.scheduler.reboot_device("System")
                self.pallete.stop()
                print("REBOOTING ....")
                return True

            events = self.poweroff.handleEvent(event)
            if 'click' in events:
                sleep(0.01)
                if not self.DEVELOPMENT:
                    self.pallete.scheduler.shutdown_device("System")
                self.pallete.stop()
                print("POWERING OFF ....")
                return True

            # return the response of the superclass
            return super(self.__class__,self).handleEvent(event)

class KeyPage(Page):

        LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
        POWER_MENU_BTN  = LOCAL_PATH + '/images/power_menu_50.png'
        WHITE           = (255, 255, 255)
        MYFONT_29       = pygame.font.SysFont("monospace", 29)
        MYFONT_50       = pygame.font.SysFont("monospace", 50)
        MYFONT_85       = pygame.font.SysFont("monospace", 85)
        KEY_LABEL       = MYFONT_50.render("Api Key", 1, WHITE)


        def __init__(self, pallete, manager, prevPage=None, nextPage=None):
            super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
            self.POWER_MENU_PAGE = RebootPage(self.pallete, self.manager, prevPage=self)
            BTN_H           = 50
            BTN_L           = 50
            BTN1_X          = self.WINDOW_WIDTH/2 - BTN_L/2
            BTN1_Y          = self.WINDOW_HEIGHT - BTN_H

            self.button_power_menu  = pygbutton.PygButton((BTN1_X, BTN1_Y, BTN_H, BTN_L),normal=self.POWER_MENU_BTN)

        def render(self):
            super(self.__class__,self).render()

            if not self.DEVELOPMENT:
                key = self.pallete.hub["API KEY"]
            else:
                key = "TEST"

            k_label = self.MYFONT_85.render(key, 1, self.WHITE)
            ip_label = self.MYFONT_29.render(self.pallete.get_local_IP()+":5000", 1, self.WHITE)

            self.pallete.screen.blit(self.KEY_LABEL , (self.WINDOW_WIDTH/2-self.KEY_LABEL.get_width()/2, 2))
            self.pallete.screen.blit(ip_label , (10, 65))
            self.pallete.screen.blit(k_label , (10, 100))
            self.button_power_menu.draw(self.pallete.screen)

        def handleEvent(self, event):

            events = self.button_power_menu.handleEvent(event)
            if 'click' in events:
                sleep(0.01)
                self.manager.setCurrentPage(self.POWER_MENU_PAGE)
                return True

            # return the response of the superclass
            return super(self.__class__,self).handleEvent(event)
