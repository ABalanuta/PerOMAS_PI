#!/usr/bin/env python
"""Represents an Action created by an user"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


class ActionsTypes():
    
    #ACTIONS and their types
    ACTION_SET_LIGHTS       = { "name":"Set_Lights", "inputs": { "Light_Bulb_1":"checkbox", "Light_Bulb_2":"checkbox" } }
    ACTION_SET_SETPOINT     = { "name":"Set_Setpoint", "inputs": { "Setpoint":"text" } }
    ACTIONS_LIST 			= [ACTION_SET_LIGHTS, ACTION_SET_SETPOINT]

class EventsTypes():
    
    #Events and their types
    EVENT_IN_THE_OFFICE	= {"name":"In_the_Office", "conditions":{"True":"True", "False":"False"}, "argument":None}
    EVENT_HUMIDITY		= {"name":"Humidity", "conditions":{"Bigger":">", "Smaller":"<"}, "argument":{ "Humidity":"text" }, "unit":"%"}
    EVENT_LIST 			= [EVENT_IN_THE_OFFICE, EVENT_HUMIDITY]


class UserAction():

    def __init__(self, alias, action, arg_type=None, arguments=None):
        self.alias = alias
        self.action = action
        self.arg_type = arg_type
        self.arguments = arguments

class UserEvent():

    def __init__(self, alias, event, condition, argument=None):
        self.alias = alias
        self.event = event
        self.condition = condition
        self.argument = argument

class UserRule():

    def __init__(self, alias, events, action):
        self.alias = alias
        self.events = events
        self.action = action