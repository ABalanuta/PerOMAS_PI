#!/usr/bin/env python
"""Represents an Actions, Events and Rules created by an user"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


class UserAction():

    def __init__(self, alias, action, arg_type=None, arguments=None, user=None):
        self.alias  = alias
        self.action = action
        self.arg_type = arg_type
        self.arguments = arguments
        self.user = user
        self.applied = False
        self.before_arguments = None

    def execute(self):
        print "Executing "+self.alias+"...."

        action_info = self.get_action_info()

        if action_info and not self.applied:
            action_info["execute"](self)
            self.applied = True
    
    def clean(self):
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
            print "UserAction.execute_set_lights " + str(self.arguments)
        
        else:
            relay.set_lights_state(self.before_arguments)
            print "UserAction.clean_set_lights " + str(self.before_arguments)

    def execute_set_setpoint(self, clean=False):
        pass

class UserEvent():

    DEBUG = True

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
            else:
                return False
        else:
            return False



    def validate_humidity(self):
        return False

class UserRule():

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
                print event.alias, False
                break
            else:
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

    ACTION_SET_SETPOINT     = { "name":"Set_Setpoint",
                                "inputs": { "Setpoint":"text" },
                                "execute":UserAction.execute_set_setpoint
                                }
    
    ACTIONS_LIST            = [ACTION_SET_LIGHTS, ACTION_SET_SETPOINT]

class EventsTypes():
    
    #Events and their types
    EVENT_IN_THE_OFFICE = { "name":"In_the_Office",
                            "conditions":{"True":"True", "False":"False"},
                            "argument":None,
                            "validate":UserEvent.validate_in_the_office
                            }
    
    EVENT_HUMIDITY      = { "name":"Humidity",
                            "conditions":{"Bigger":">", "Smaller":"<"},
                            "argument":{"Humidity":"text" },
                            "validate":UserEvent.validate_humidity,
                            "unit":"%"
                            }
    
    EVENT_LIST          = [EVENT_IN_THE_OFFICE, EVENT_HUMIDITY]