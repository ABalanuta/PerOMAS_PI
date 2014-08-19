#!/usr/bin/env python
"""Manages the WebUsers and their Passwords"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
import base64
import hashlib
from datetime import datetime

from UserRules import *


class PasswordManager():

    STRECHING = 87  # Number of times the Hash function is called

    def getDigest(self, user, password, salt=None):

        if not salt:
            salt = base64.b64encode(os.urandom(64))

        digest = hashlib.sha512(
            str(salt) + str(user) + str(password)).hexdigest()
        for x in range(0, self.STRECHING):
            digest = hashlib.sha512(
                str(salt) + str(user) + str(digest)).hexdigest()

        return salt, digest

    def isPassword(self, user, password, salt, digest):
        return self.getDigest(user, password, salt)[1] == digest




class User(object):

    def __init__(self, username, salt, digest, manager, phone=None, hub=None, setpoint=24):
        self.hub = hub
        self.username = username
        self.salt = salt
        self.digest = digest
        self.phone = phone
        self.setpoint = setpoint
        self.manager = manager
        self.actions = list()
        self.events = list()
        self.rules = list()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)
    
    def get_phone(self):
        return self.phone

    def set_phone(self, mac):
        self.phone = mac
        # Alter user in DB
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            db.alterUser(self)

    def set_setpoint(self, new_setpoint):
        
        # Alter user in DB
        if self.hub:
            db          = self.hub["STORAGE HANDLER"]
            temp        = self.hub["TEMPERATURE"].temp
            humid       = self.hub["HUMIDITY"].humid
            ext_temp    = self.hub["EXTERNAL TEMPERATURE"].temp
            ext_humid   = self.hub["EXTERNAL HUMIDITY"].humid
            lux         = self.hub["LUMINOSITY"].lux
            current     = self.hub["CURRENT"].watts

            db.alterUser(self)
            db.addUserFeedback(self.username, datetime.now(), self.setpoint, new_setpoint,
                                temp, humid, ext_temp, ext_humid, lux, current)

        self.setpoint = new_setpoint


    def add_action(self, alias, action, arg_type=None, arguments=None):
        action = UserAction(alias, action, arg_type, arguments)
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            db.alterUserDetails("Add", "Action", self.username, action)
        action.user = self
        self.actions.append(action)

    def add_event(self, alias, event, condition, argument=None):
        event = UserEvent(alias, event, condition, argument)
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            db.alterUserDetails("Add", "Event", self.username, event)
        event.user = self
        self.events.append(event)

    def add_rule(self, alias, events, action):
        rule = UserRule(alias, events, action)
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            db.alterUserDetails("Add", "Rule", self.username, rule)
        rule.user = self
        self.rules.append(rule)

    def del_action(self, alias):
        for action in self.actions:
            if action.alias == alias:
                self.actions.remove(action)
                if self.hub:
                    db = self.hub["STORAGE HANDLER"]
                    db.alterUserDetails("Del", "Action", self.username, action)

    def del_event(self, alias):
        for event in self.events:
            if event.alias == alias:
                self.events.remove(event)
                if self.hub:
                    db = self.hub["STORAGE HANDLER"]
                    db.alterUserDetails("Del", "Event", self.username, event)

    def del_rule(self, alias):
        for rule in self.rules:
            if rule.alias == alias:
                self.rules.remove(rule)
                if self.hub:
                    db = self.hub["STORAGE HANDLER"]
                    db.alterUserDetails("Del", "Rule", self.username, rule)

    def get_action(self, alias):
        for action in self.actions:
            if action.alias == alias:
                return action
        return None

    def get_event(self, alias):
        for event in self.events:
            if event.alias == alias:
                return event
        return None


    def has_action_alias(self, alias):
        for action in self.actions:
            if action.alias == alias:
                return True
        return False

    def has_event_alias(self, alias):
        for event in self.events:
            if event.alias == alias:
                return True
        return False

    def has_rule_alias(self, alias):
        for rule in self.rules:
            if rule.alias == alias:
                return True
        return False


    def __repr__(self):
        return '<User %r>' % (self.username)


class UserManager():

    def __init__(self, hub=None):
    	self.hub = hub
        self.users = dict()
        self.password_manager = PasswordManager()
        self.actionsTypes = ActionsTypes()
        self.eventTyeps = EventsTypes()
        self.loadUsers()
        self.loadUsersDetails()

    def addUser(self, username, password):

        salt, digest = self.password_manager.getDigest(username, password)
        newUser = User(username, salt, digest, self, hub=self.hub)
        self.users[username] = newUser

        # Add user do DB
        if self.hub:
        	db = self.hub["STORAGE HANDLER"]
        	db.addUser(newUser)

    def loadUsers(self):
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            matrix = db.loadUsers()
            for x in matrix:
                self.users[x[0]] = User(x[0], x[1], x[2], self, phone=x[3], hub=self.hub, setpoint=x[4])
        else:
            print "Error Loading Users"

    def loadUsersDetails(self):
        if self.hub:
            db = self.hub["STORAGE HANDLER"]
            d = db.loadUsersDetails()
            for x in d:
                u = self.getUser(x[0])
                if x[1] == "Action":
                    detail = x[3]
                    detail.user = u
                    u.actions.append(detail)
                elif x[1] == "Event":
                    detail = x[3]
                    detail.user = u
                    u.events.append(detail)
                elif x[1] == "Rule":
                    detail = x[3]
                    detail.user = u
                    u.rules.append(detail)
        else:
            print "Error Loading Users Details"

    def getUser(self, username):
        if self.existsUser(username):
            return self.users[username]
        else:
            return None

    def existsUser(self, username):

        if username in self.users.keys():
            return True
        else:
            return False
    

    def validatePassword(self, username, password):
        u = self.getUser(username)
        if u:
            return self.password_manager.isPassword(username,
                                                    password,
                                                    u.salt,
                                                    u.digest)
        else:
			return False


if __name__ == "__main__":


    um = UserManager()
    um.addUser("Artur", "teste")

    print um.existsUser("Artur")
    print um.getUser("Artur")

    print um.validatePassword("artur", "Cenora")
    print um.validatePassword("Artur", "Cenora")
    print um.validatePassword("Artur", "teste")
