#!/usr/bin/env python
"""Represents an Actions, Events and Rules created by an user"""

__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


class UserAction():

    def __init__(self, alias, action, arg_type=None, arguments=None, user=None):
        self.alias = alias
        self.action = action
        self.arg_type = arg_type
        self.arguments = arguments
        self.user = user

    def execute(self):
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
        #self.get_aux().validate()
        return False
    
    def get_aux(self):
        for event in EventsTypes.EVENT_LIST:
            if event["name"] == self.event:
                return event
        return None

    def validate_in_the_office(self):
        if self.DEBUG:
            print "validate_in_the_office "+ self.user.username
        pass

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
                break

        #If all events are valid then execute the action
        if can_execute_action:
            self.action.execute()

        return can_execute_action
            

class ActionsTypes():
    
    #ACTIONS and their types
    ACTION_SET_LIGHTS       = { "name":"Set_Lights",
                                "inputs": { "Light_Bulb_1":"checkbox", "Light_Bulb_2":"checkbox" }
                                }

    ACTION_SET_SETPOINT     = { "name":"Set_Setpoint",
                                "inputs": { "Setpoint":"text" }
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
                            "unit":"%"
                            }
    
    EVENT_LIST          = [EVENT_IN_THE_OFFICE, EVENT_HUMIDITY]