#!/usr/bin/env python
"""Manages the WebUsers and their Passwords"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


import base64
import hashlib
import os


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

    def __init__(self, username, salt, digest, phone=None, hub=None):
        self.hub = hub
        self.username = username
        self.salt = salt
        self.digest = digest
        self.phone = phone

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

    def __repr__(self):
        return '<User %r>' % (self.username)


class UserManager():

    def __init__(self, hub=None):
    	self.hub = hub
        self.users = dict()
        self.password_manager = PasswordManager()
        self.loadUsers()

    def addUser(self, username, password):

        salt, digest = self.password_manager.getDigest(username, password)
        newUser = User(username, salt, digest, hub=self.hub)
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
                self.users[x[0]] = User(x[0], x[1], x[2], phone=x[3], hub=self.hub)
        else:
            print "Error Loading Users"

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
