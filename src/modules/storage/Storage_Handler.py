#!/usr/bin/env python
"""Manages the storage of the values
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import sqlite3
import os
from time import sleep
from threading import Thread
from datetime import datetime
from MesurmentDTO import MesurmentDTO
from MeasurmentEnum import DataType
class StorageHandler(Thread):
	
	DEBUG 		= False
	FILENAME 	= 'database.sqlite3.db'
	
	def __init__(self, hub):
		Thread.__init__(self)
		
		self.hub = hub
		self.stopped = True
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.db_path = dir_path +'/' + self.FILENAME
		
		self.create_database()
		
	def stop(self):
		self.stopped = True
	
	def run(self):
		self.stopped = False
		while not self.stopped:
			self.update()
			
	def update(self):
		if self.DEBUG:
			print "Update"
	
	def create_database(self):
		
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		#Try to create the empty Tables if they dont already exist
		try:
			c.execute('CREATE TABLE '+DataType.TEMPERATURE+' (TimeStamp TIMESTAMP, '+DataType.TEMPERATURE+' REAL)')
			c.execute('CREATE TABLE '+DataType.HUMIDITY+' (TimeStamp TIMESTAMP, '+DataType.HUMIDITY+' REAL)')
			c.execute('CREATE TABLE '+DataType.LUMINOSITY+' (TimeStamp TIMESTAMP, '+DataType.LUMINOSITY+' REAL)')
			c.execute('CREATE TABLE '+DataType.CURRENT+' (TimeStamp TIMESTAMP, '+DataType.CURRENT+' REAL)')
		except:
			if self.DEBUG:
				print "Database " + self.FILENAME + " Already Exists, skipping ..."
		finally:
			conn.commit()
			conn.close()
	
	def insertValue(self, dto):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		values = (dto.getTimestamp(), dto.getValue())
		c.execute('INSERT INTO '+dto.getType()+' VALUES (?,?)', values)
		conn.commit()
		conn.close()
		
	def get_all_temp(self):
		#query = '''
		#	SELECT * 
		#	FROM ambient
		#	ORDER BY datetime DESC 
		#	LIMIT 1;
		#	'''
		#c.execute(query)
		#all = c.fetchall()
		#print all
		
		return
		
		
		
#Runs only if called
if __name__ == "__main__":
	
	d = StorageHandler(None)
	d.start()
	
	
	print "ola"
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, 28.4))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, 50.1))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, 200))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, 3000))
	
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.TEMPERATURE, 23.4))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.HUMIDITY, 51.1))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.LUMINOSITY, 230))
	d.insertValue(MesurmentDTO(str(datetime.now()), DataType.CURRENT, 3100.33))
	
	print "adeus"
	d.stop()
	d.join()

	
	
	
	
	
	

