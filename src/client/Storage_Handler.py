#!/usr/bin/env python
"""Manages the storage of the values
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.1"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import sqlite3
import os
from time import sleep
from datetime import datetime
from threading import Lock
from pickle import dumps, loads
from DTOs.MesurmentDTO import MesurmentDTO
from DTOs.MeasurmentEnum import DataType

class StorageHandler():
	
	DEBUG 		= True
	FILENAME 	= 'database.sqlite3.db'
	
	def __init__(self, hub):
		
		self.hub = hub
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.db_path = dir_path +'/' + self.FILENAME
		self.db_lock = Lock()
		self.create_database()
		
	
	def create_database(self):
		
		self.db_lock.acquire(True)

		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		#Try to create the empty Tables if they dont already exist
		try:

			#Settings
			c.execute('CREATE TABLE Settings (ID TEXT, PickeRepresentation TEXT)')


			#Data
			c.execute('CREATE TABLE '+DataType.TEMPERATURE+' (TimeStamp TIMESTAMP, Temperature REAL)')
			c.execute('CREATE TABLE '+DataType.HUMIDITY+' (TimeStamp TIMESTAMP, Humidity REAL)')
			c.execute('CREATE TABLE '+DataType.LUMINOSITY+' (TimeStamp TIMESTAMP, Luminosity REAL)')
			c.execute('CREATE TABLE '+DataType.CURRENT+' (TimeStamp TIMESTAMP, Current REAL)')
			c.execute('CREATE TABLE '+DataType.BT_PRESENCE+' (TimeStamp TIMESTAMP, MAC TEXT)')
			c.execute('CREATE TABLE '+DataType.WIFI_PRESENCE+' (TimeStamp TIMESTAMP, MAC TEXT, LOCATIONS TEXT)')

			if self.DEBUG:
				print "New Database " + self.FILENAME + " Created"

		except sqlite3.OperationalError:
			if self.DEBUG:
				print "Database " + self.FILENAME + " Already Exists, skipping ..."
		except:
			raise

		finally:
			conn.commit()
			conn.close()
			self.db_lock.release()
	
	def insertValue(self, dto):

		self.db_lock.acquire(True)

		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()

		if len(dto.getValue()) == 1:
			values = (dto.getTimestamp(), dto.getValue()[0])
			c.execute('INSERT INTO '+dto.getType()+' VALUES (?,?)', values)

		elif len(dto.getValue()) == 2:
			values = (dto.getTimestamp(), dto.getValue()[0], dto.getValue()[1])
			c.execute('INSERT INTO '+dto.getType()+' VALUES (?,?,?)', values)

		else:
			raise Exception("Too many Fields")

		conn.commit()
		conn.close()

		self.db_lock.release()

	def readSettings(self, id):
		self.db_lock.acquire(True)

		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute('SELECT * FROM Settings WHERE ID=?', [id])
		settings = c.fetchone()
		if settings:
			settings = loads(settings[1])
		conn.commit()
		conn.close()
		self.db_lock.release()
		return settings
	
	def writeSettings(self, id, obj):
		self.db_lock.acquire(True)

		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		encoded = dumps(obj)
		values = (id, encoded)
		c.execute('DELETE FROM Settings WHERE ID=?', [id])
		c.execute('INSERT INTO Settings VALUES (?,?)', values)
		conn.commit()
		conn.close()

		self.db_lock.release()

	#Bogus method
	def stop(self):
		return
		
#Runs only if called
if __name__ == "__main__":
	
	d = StorageHandler(None)
	
	print "Insert"
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, 28.4))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, 50.1))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, 200))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, 3000))
	
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, 23.4))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, 51.1))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, 230))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, 3100.33))
	
	print "Done"

	t = {"Sapos":123, "COGUMELOS":[1,2,3]}

	d.writeSettings("teste", t)
	print d.readSettings("teste")
	

