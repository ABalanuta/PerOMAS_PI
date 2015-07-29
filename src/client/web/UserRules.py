#!/usr/bin/env python
"""Represents an Actions, Events and Rules created by an user"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from time import localtime, time as now_time
from datetime import time

class UserAction():

    DEBUG = False

    def __init__(self, alias, action, arg_type=None, arguments=None, user=None):
        self.alias  = alias
        self.action = action
        self.arg_type = arg_type
        self.arguments = arguments
        self.user = user
        self.applied = False
        self.before_arguments = None

    def execute(self):
        if self.DEBUG:
            print "Executing "+self.alias+"...."

        action_info = self.get_action_info()

        if action_info and not self.applied:
            action_info["execute"](self)
            self.applied = True
    
    def clean(self):

        if self.DEBUG:
            print "Cleaning "+self.alias+"...."

        action_info = self.get_action_info()

        if self.applied:
            action_info["execute"](self, clean=True)
            self.applied = False

    def get_action_info(self):
        for action_info in ActionsTypes.ACTIONS_LIST:
            if action_info["name"] == self.action:
                return action_info
        return None

    def execute_set_lights(self, clean=False):
        relay = self.user.hub["RELAY"]
        
        if not clean:
            self.before_arguments = relay.get_lights_state()
            relay.set_lights_state(self.arguments)
            if self.DEBUG:
                print "UserAction.execute_set_lights " + str(self.arguments)
        
        else:
            relay.set_lights_state(self.before_arguments)
            if self.DEBUG:
                print "UserAction.clean_set_lights " + str(self.before_arguments)

class UserEvent():

    DEBUG = False

    def __init__(self, alias, event, condition, argument=None, user=None):
        self.alias = alias
        self.event = event
        self.condition = condition
        self.argument = argument
        self.user = user
        
    def is_valid(self):
        event_info = self.get_event_info()

        if event_info:
            return event_info["validate"](self)
        else:
            return False
    
    def get_event_info(self):
        for event_info in EventsTypes.EVENT_LIST:
            if event_info["name"] == self.event:
                return event_info
        return None

    def validate_in_the_office(self):

        phone_mac = self.user.phone

        #Phone must be defined
        if not phone_mac:
            return False

        if "BLUETOOTH" in self.user.hub.keys():
            if phone_mac in self.user.hub["BLUETOOTH"].get_traked_devices():
                return True
                if self.DEBUG:
                    print "UserEvent.validate_in_the_office " + str(True)
            else:
                if self.DEBUG:
                    print "UserEvent.validate_in_the_office " + str(False)
                return False
        else:
            return False



    def validate_time(self):

        lt = localtime(now_time())
        current_time = time(lt.tm_hour, lt.tm_min)
        t1, t2 = self.argument.split("-")
        h1, m1 = t1.split(':')
        h2, m2 = t2.split(':')
        t1, t2 = time(int(h1), int(m1)), time(int(h2), int(m2))
        
        if t1 == t2:
            return False

        inverse = False
        

        #If the time interval passes the midnight mark, the exclusion rule is aplied
        if t1 > t2:
            inverse = True  # inverses the logical response
            t1, t2 = t2, t1 # inverses the time interval

        ret = False
        if current_time >= t1 and current_time <= t2:
            ret = True

        if inverse:
            return not ret
        else:
            return ret

class UserRule():

    DEBUG = False
    
    def __init__(self, alias, events, action, user=None):
        self.alias = alias
        self.events = events
        self.action = action
        self.user = user

    def try_execute(self):
        
        if not self.user:
            return False

        can_execute_action = True

        for event_alias in self.events:
            event = self.user.get_event(event_alias)

            #Validates all the events
            if not event or not event.is_valid():
                can_execute_action = False
                if self.DEBUG:
                    print event.alias, False
                break
            else:
                if self.DEBUG:
                    print event.alias, True

        action = self.user.get_action(self.action)
        
        if not action:
            return False

        #If all events are valid then execute the action
        if can_execute_action:
            action.execute()
        else:
            action.clean()

        return can_execute_action
            

class ActionsTypes():
    
    #ACTIONS and their types
    ACTION_SET_LIGHTS       = { "name":"Set_Lights",
                                "inputs": { "Light_Bulb_1":"checkbox",
                                            "Light_Bulb_2":"checkbox" },
                                "execute":UserAction.execute_set_lights
                                }
    
    ACTIONS_LIST            = [ACTION_SET_LIGHTS]

class EventsTypes():
    
    #Events and their types
    EVENT_IN_THE_OFFICE = { "name":"In_the_Office",
                            "conditions":{"True":"True"},
                            "argument":None,
                            "validate":UserEvent.validate_in_the_office
                            }
    
    EVENT_TIME      = { "name":"Time",
                            "conditions":{ "Interval":"Interval" },
                            "argument":{"Time":"text" },
                            "validate":UserEvent.validate_time,
                            "unit":"H:m-H:m"
                            }
    
    EVENT_LIST          = [EVENT_IN_THE_OFFICE, EVENT_TIME]