#!/usr/bin/env python
"""Manages the storage of the values
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import os
from time import sleep
from datetime import datetime
from threading import Lock
from pickle import dumps, loads
from DTOs.MesurmentDTO import MesurmentDTO
from DTOs.MeasurmentEnum import DataType


import MySQLdb


class StorageHandler():
	
	DEBUG 		= True
	HOST 		= "localhost"
	USER 		= "root"
	PASS 		= "3O7DCWP2HLR01471G9PZQ6U7X"
	DB 			= "PeromasDB"

	def __init__(self, hub):
		
		self.hub = hub
		#self.delete_database(self.DB)
		#self.create_database(self.DB)

	def create_database(self, DB):
		if self.DEBUG:
				print "create_database "+DB

		db = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS)
		cursor = db.cursor()
		try:
			cursor.execute('CREATE DATABASE '+DB)
			db.commit()
			if self.DEBUG:
				print "	Database Created"

			self.popolate_database()

		except:

			if self.DEBUG:
				print "	Database already Present"
		db.close()

	def delete_database(self, DB):
		if self.DEBUG:
				print "delete_database "+DB

		db = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS)
		cursor = db.cursor()
		try:
			cursor.execute('DROP DATABASE '+DB)
			db.commit()
			if self.DEBUG:
				print "	Database Deleted"
		except:
			if self.DEBUG:
				print "	Database does not Exist"
		db.close()
		
	
	def popolate_database(self):
		
		db = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = db.cursor()
		#Try to create the empty Tables if they dont already exist
		try:
			#Users
			c.execute('CREATE TABLE Logs (TimeStamp TIMESTAMP, Username TEXT, Message TEXT)')
			c.execute('CREATE TABLE Users (Username TEXT, Salt TEXT, Digest TEXT)')
			c.execute('CREATE TABLE BTDevices (BTDevice TEXT, Username TEXT)')

			#Settings
			c.execute('CREATE TABLE Settings (ID TEXT, PickeRepresentation TEXT)')

			#Data
			c.execute('CREATE TABLE '+DataType.TEMPERATUREHUMIDITY+' (TimeStamp TIMESTAMP, Temperature REAL, Humidity REAL)')
			c.execute('CREATE TABLE '+DataType.LUMINOSITY+' (TimeStamp TIMESTAMP, Luminosity REAL)')
			c.execute('CREATE TABLE '+DataType.CURRENT+' (TimeStamp TIMESTAMP, Current REAL)')
			c.execute('CREATE TABLE '+DataType.BT_PRESENCE+' (TimeStamp TIMESTAMP, MAC TEXT)')
			c.execute('CREATE TABLE '+DataType.WIFI_PRESENCE+' (TimeStamp TIMESTAMP, MAC TEXT, LOCATIONS TEXT)')
			db.commit()

			if self.DEBUG:
				print "	Database Popolated"

		except:
			raise

		finally:
			db.close()
	
	def insertValue(self, dto):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()

		if len(dto.getValue()) == 1:
			values = (dto.getTimestamp(), dto.getValue()[0])
			c.execute('INSERT INTO '+dto.getType()+' VALUES (%s, %s)', values)


		elif len(dto.getValue()) == 2:
			values = (dto.getTimestamp(), dto.getValue()[0], dto.getValue()[1])
			c.execute('INSERT INTO '+dto.getType()+' VALUES (%s, %s, %s)', values)

		else:
			conn.close()
			raise Exception("Too many Fields")

		conn.commit()
		conn.close()

	def addUser(self, user):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()

		values = (user.username, user.salt, user.digest)
		c.execute('INSERT INTO Users VALUES (%s, %s, %s)', values)

		conn.commit()
		conn.close()

	def loadUsers(self):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()

		c.execute('SELECT * FROM Users')
		resp = c.fetchall()

		conn.commit()
		conn.close()
		return resp

	def getGraphData(self):

		data = {}

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()

		c.execute("SELECT TimeStamp, Temperature, Humidity FROM TemperatureHumidity WHERE TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL 1 DAY ")
		data["TempHumid"] = c.fetchall()

		c.execute("SELECT * FROM Luminosity WHERE TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL 1 DAY ")
		data["Luminosity"] = c.fetchall()

		c.execute("SELECT * FROM Current WHERE TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL 1 DAY ")
		data["Current"] = c.fetchall()

		
		conn.commit()
		conn.close()
		return data

	def readSettings(self, id):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()
		c.execute('SELECT * FROM Settings WHERE ID=%s', [id])
		settings = c.fetchone()
		if settings:
			settings = loads(settings[1])
		conn.commit()
		conn.close()
		return settings
	
	def writeSettings(self, id, obj):
		
		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()
		encoded = dumps(obj)
		values = (id, encoded)
		c.execute('DELETE FROM Settings WHERE ID=%s', [id])
		c.execute('INSERT INTO Settings VALUES (%s, %s)', values)
		conn.commit()
		conn.close()

	def log(self, msg, user = "Pi Robot"):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()
		values = (datetime.now(), user, msg.encode('ascii', 'ignore'))
		c.execute('INSERT INTO Logs VALUES (%s, %s, %s)', values)
		conn.commit()
		conn.close()
	
	def getLogs(self, num):

		conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASS, db=self.DB)
		c = conn.cursor()
		values = (num)
		c.execute('SELECT * FROM Logs ORDER BY TimeStamp DESC LIMIT %s', values)
		data = c.fetchall()
		conn.commit()
		conn.close()
		return data


	#Bogus method
	def stop(self):
		return
		
#Runs only if called
if __name__ == "__main__":
	
	d = StorageHandler(None)
	
	#print "Insert"
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, [28.4]))
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, [50.1]))


	#date = datetime.now()

	#d.insertValue(MesurmentDTO(str(date), DataType.TEMPERATURE, [28.4]))
	#d.insertValue(MesurmentDTO(str(date), DataType.HUMIDITY, [50.1]))


	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, [200]))
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, [3000]))
	
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, [23.4]))
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, [51.1]))
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, [230]))
	#d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, [3100.33]))
	
	#print "Done"

	#t = {"Sapos":123, "COGUMELOS":[1,2,3]}

	#d.writeSettings("teste", t)
	#print d.readSettings("teste")
	#for x, y in d.getGraphData().items():
	#	print x, y	
	
		
	#create_database(DB)
	#delete_database(DB)
	#delete_database(DB)
	#db = connect(host=HOST, user=USER, passwd=PASS,db=DB)
	
	
