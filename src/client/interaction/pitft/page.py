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
    IMG_EXIT        = LOCAL_PATH + '/images/leave_50_a.png'
    IMG_ENTER       = LOCAL_PATH + '/images/enter_50_c.png'


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
        self.button_exit_enter = pygbutton.PygButton((BTN_E_X, BTN_E_Y, BTN_E_H, BTN_E_L),normal=self.IMG_EXIT)

        self.savedState = False

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

        if self.savedState:
            self.button_exit_enter.setSurfaces(self.IMG_ENTER)
        else:
            self.button_exit_enter.setSurfaces(self.IMG_EXIT)


        self.button_light_1.draw(self.pallete.screen)
        self.button_light_2.draw(self.pallete.screen)
        self.button_exit_enter.draw(self.pallete.screen)

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

        events = self.button_exit_enter.handleEvent(event)
        if 'click' in events:

            # preform the exit routine
            if self.savedState:
                self.savedState = False
                if not self.DEVELOPMENT:
                    #Load the previous state
                    self.pallete.relay.set_lights_x1_state(self.light1_state)
                    self.pallete.relay.set_lights_x2_state(self.light2_state )
                    self.pallete.relay.set_ac_speed(self.speed_state)
                    self.pallete.logic.setACMode(self.logic_state)
                else:
                     self.x1 = self.light1_state
                     self.x2 = self.light2_state
            else:
                self.savedState = True
                if not self.DEVELOPMENT:
                    #Save the state
                    self.light1_state = self.pallete.relay.get_lights_x1_state()
                    self.light2_state = self.pallete.relay.get_lights_x2_state()
                    self.speed_state = self.pallete.relay.get_ac_speed()
                    self.logic_state = self.pallete.logic.getACMode()
                    #Shut down the subsystems
                    self.pallete.relay.set_lights_x1_state(False)
                    self.pallete.relay.set_lights_x2_state(False)
                    self.pallete.logic.setACMode("Manual")
                    self.pallete.relay.set_ac_speed(0)
                else:
                    #Save the state
                    self.light1_state = self.x1
                    self.light2_state = self.x2

                    self.x1 = False
                    self.x2 = False
            return True

        # return the response of the superclass
        return super(self.__class__,self).handleEvent(event)

class ACManualPage(Page):
    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    IMG_MANUAL      = LOCAL_PATH + '/images/manual_60.png'
    IMG_AUTO        = LOCAL_PATH + '/images/auto_60.png'
    MYFONT_50       = pygame.font.SysFont("monospace", 50)
    MYFONT_25       = pygame.font.SysFont("monospace", 25)
    MYFONT_35       = pygame.font.SysFont("monospace", 35)
    WHITE           = (255, 255, 255)
    BLACK           = (  0,   0,   0)
    BLUE            = (  0,   0, 255)
    RED             = (255,   0,   0)
    RED2            = (232,   0,  66)
    YELLOW          = (255, 204,  51)
    LIGHT_BLUE      = ( 51, 204, 255)

    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
        self.modeName = "Manual"
        BTN_M_H         = 60
        BTN_M_L         = 60
        BTN_M_X          = self.WINDOW_WIDTH - BTN_M_L
        BTN_M_Y          = self.WINDOW_HEIGHT - BTN_M_H

        B0_H = 60
        B0_L = 60
        B0_X = (self.WINDOW_WIDTH/4 - B0_L)/2
        B0_Y = self.WINDOW_HEIGHT/10

        B1_H = 60
        B1_L = 60
        B1_X = 3*B0_X + B0_L
        B1_Y = B0_Y

        B2_H = 60
        B2_L = 60
        B2_X = 5*B0_X + B0_L + B1_L
        B2_Y = B0_Y

        B3_H = 60
        B3_L = 60
        B3_X = 7*B0_X + B0_L + B1_L + B2_L
        B3_Y = B0_Y

        BH_H = 60
        BH_L = 120
        BH_X = (self.WINDOW_WIDTH/2 - BH_L)/2
        BH_Y = B0_Y*2 + B0_L

        BC_H = 60
        BC_L = 120
        BC_X = 3*BH_X + BH_L
        BC_Y = BH_Y

        self.button_mode    = pygbutton.PygButton((BTN_M_X, BTN_M_Y, BTN_M_H, BTN_M_L),normal=self.IMG_AUTO)
        self.button_speed_0 = pygbutton.PygButton((B0_X, B0_Y, B0_L, B0_H),"0", font=self.MYFONT_50)
        self.button_speed_1 = pygbutton.PygButton((B1_X, B1_Y, B1_L, B1_H),"1", font=self.MYFONT_50)
        self.button_speed_2 = pygbutton.PygButton((B2_X, B2_Y, B2_L, B2_H),"2", font=self.MYFONT_50)
        self.button_speed_3 = pygbutton.PygButton((B3_X, B3_Y, B3_L, B3_H),"3", font=self.MYFONT_50)
        self.button_warm    = pygbutton.PygButton((BH_X, BH_Y, BH_L, BH_H),"Warm", font=self.MYFONT_35, bgcolor=self.RED2)
        self.button_cold    = pygbutton.PygButton((BC_X, BC_Y, BC_L, BC_H),"Cold", font=self.MYFONT_35, bgcolor=self.BLUE)

        #self.button_speed_2.buttonDown = True
        if self.DEVELOPMENT:
            self.button_speed_pressed = self.button_speed_0
            self.warm = False

    def render(self):
        super(self.__class__,self).render()
        self.button_mode.draw(self.pallete.screen)

        self.button_speed_0.buttonDown = False
        self.button_speed_1.buttonDown = False
        self.button_speed_2.buttonDown = False
        self.button_speed_3.buttonDown = False
        self.button_cold.buttonDown = False
        self.button_warm.buttonDown = False


        if self.DEVELOPMENT:
            self.button_speed_pressed.buttonDown = True
            if self.warm:
                self.button_warm.buttonDown = True
            else:
                self.button_cold.buttonDown = True
        else:
            speed = self.pallete.relay.get_ac_speed()
            mode = self.pallete.relay.get_ac_mode()
            if speed == 0:
                self.button_speed_0.buttonDown = True
            if speed == 1:
                self.button_speed_1.buttonDown = True
            if speed == 2:
                self.button_speed_2.buttonDown = True
            if speed == 3:
                self.button_speed_3.buttonDown = True
            if mode == "Heat":
                self.button_warm.buttonDown = True
            else:
                self.button_warm.buttonDown = True

        self.button_speed_0.draw(self.pallete.screen)
        self.button_speed_1.draw(self.pallete.screen)
        self.button_speed_2.draw(self.pallete.screen)
        self.button_speed_3.draw(self.pallete.screen)
        self.button_warm.draw(self.pallete.screen)
        self.button_cold.draw(self.pallete.screen)

    def handleEvent(self, event):
        events = self.button_mode.handleEvent(event)
        if 'click' in events:
            print("From Manual")
            self.prev.toggleACMode()
            return True

        events = self.button_speed_0.handleEvent(event)
        if 'click' in events:
            print("Button Speed 0")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_speed(0)
            else:
                self.button_speed_pressed = self.button_speed_0
            return True
        events = self.button_speed_1.handleEvent(event)
        if 'click' in events:
            print("Button Speed 1")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_speed(1)
            else:
                self.button_speed_pressed = self.button_speed_1
            return True
        events = self.button_speed_2.handleEvent(event)
        if 'click' in events:
            print("Button Speed 2")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_speed(2)
            else:
                self.button_speed_pressed = self.button_speed_2
            return True
        events = self.button_speed_3.handleEvent(event)
        if 'click' in events:
            print("Button Speed 3")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_speed(3)
            else:
                self.button_speed_pressed = self.button_speed_3
            return True
        events = self.button_warm.handleEvent(event)
        if 'click' in events:
            print("Button Warm")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_mode("Heat")
            else:
                self.warm = True
            return True
        events = self.button_cold.handleEvent(event)
        if 'click' in events:
            print("Button Cold")
            if not self.DEVELOPMENT:
                self.pallete.relay.set_ac_mode("Cool")
            else:
                self.warm = False
            return True
        # return the response of the superclass
        return super(self.__class__,self).handleEvent(event)

class ACAutoPage(Page):
    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    WHITE           = (255, 255, 255)
    MYFONT_70       = pygame.font.SysFont("monospace", 70)
    MYFONT_55       = pygame.font.SysFont("monospace", 55)
    IMG_MANUAL      = LOCAL_PATH + '/images/manual_60.png'
    IMG_AUTO        = LOCAL_PATH + '/images/auto_60.png'

    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)
        self.modeName = "Auto"
        BTN_M_H = 60
        BTN_M_L = 60
        BTN_M_X = self.WINDOW_WIDTH - BTN_M_L
        BTN_M_Y = self.WINDOW_HEIGHT - BTN_M_H

        BP_H = 60
        BP_L = 60
        BP_X = (self.WINDOW_WIDTH/8)*6
        BP_Y = (self.WINDOW_HEIGHT/8)*3 - BP_H

        BM_H = 60
        BM_L = 60
        BM_X = (self.WINDOW_WIDTH/8)*6
        BM_Y = (self.WINDOW_HEIGHT/8)*3

        self.button_mode = pygbutton.PygButton((BTN_M_X, BTN_M_Y, BTN_M_H, BTN_M_L),normal=self.IMG_MANUAL)
        self.button_plus = pygbutton.PygButton((BP_X, BP_Y, BP_L, BP_H),"+", font=self.MYFONT_70)
        self.button_minus = pygbutton.PygButton((BM_X, BM_Y, BM_L, BM_H),"-", font=self.MYFONT_70)


        if self.DEVELOPMENT:
            self.setpoint = 24.0

    def render(self):
        super(self.__class__,self).render()

        if not self.DEVELOPMENT:
            setpoint  = round(self.pallete.logic.get_AC_Setpoint(), 1)
        else:
            setpoint = self.setpoint

        s_label = self.MYFONT_55.render(str(setpoint)+" C"+chr(176), 1, self.WHITE)
        self.pallete.screen.blit(s_label , (10, 60))

        self.button_mode.draw(self.pallete.screen)
        self.button_plus.draw(self.pallete.screen)
        self.button_minus.draw(self.pallete.screen)

    def handleEvent(self, event):
        events = self.button_mode.handleEvent(event)
        if 'click' in events:
            print("From Auto")
            self.prev.toggleACMode()
            return True
        events = self.button_plus.handleEvent(event)
        if 'click' in events:
            if self.DEVELOPMENT:
                if self.setpoint < 40:
                    self.setpoint = self.setpoint + 0.5
            else:
                if self.setpoint < 40:
                    setpoint = self.pallete.logic.get_AC_Setpoint()
                    self.pallete.logic.set_AC_Setpoint(setpoint + 0.5)

            return True
        events = self.button_minus.handleEvent(event)
        if 'click' in events:
            if self.DEVELOPMENT:
                if self.setpoint > 10:
                    self.setpoint = self.setpoint - 0.5
            else:
                if self.setpoint > 10:
                    setpoint = self.pallete.logic.get_AC_Setpoint()
                    self.pallete.logic.set_AC_Setpoint(setpoint - 0.5)
            return True
        # return the response of the superclass
        return super(self.__class__,self).handleEvent(event)

class TemperaturePage(Page):

    LOCAL_PATH      = os.path.dirname(os.path.realpath(__file__))
    COGWHEEL_BTN    = LOCAL_PATH + '/images/gears_50_a.png'
    WHITE           = (255, 255, 255)
    MYFONT_85       = pygame.font.SysFont("monospace", 85)

    def __init__(self, pallete, manager, prevPage=None, nextPage=None):
        super(self.__class__,self).__init__(pallete, manager, prevPage=prevPage, nextPage=nextPage)

        BTN_H           = 50
        BTN_L           = 50
        BTN1_X          = self.WINDOW_WIDTH/2 - BTN_L/2
        BTN1_Y          = self.WINDOW_HEIGHT - BTN_H

        self.button_cogwheel  = pygbutton.PygButton((BTN1_X, BTN1_Y, BTN_H, BTN_L),normal=self.COGWHEEL_BTN)

        self.manual     = ACManualPage(self.pallete, self.manager, prevPage=self)
        self.auto       = ACAutoPage(self.pallete, self.manager, prevPage=self)

        if self.DEVELOPMENT:
            self.AC_MENU = self.manual
        else:
            self.AC_MENU = self.auto


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

    def toggleACMode(self):
        if self.DEVELOPMENT:
            if self.AC_MENU.modeName == "Manual":
                print("Manual->Auto")
                self.AC_MENU = self.auto
            else:
                print("Auto->Manual")
                self.AC_MENU = self.manual
        else:
            mode = self.pallete.logic.getACMode()
            if mode == "Manual":
                self.pallete.logic.setACMode("Auto")
                self.AC_MENU = self.auto
            else:
                self.pallete.logic.setACMode("Manual")
                self.AC_MENU = self.manual
        self.manager.setCurrentPage(self.AC_MENU)

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
        POWER_MENU_BTN  = LOCAL_PATH + '/images/plug_50_a.png'
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
