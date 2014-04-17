#!/usr/bin/env python
"""A base class that represents a mesurment taken by a sensor"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


class MesurmentDTO():
	
	value = None
	dto_type = None
	timestamp = None
	
	def __init__(self, timestamp, dto_type, value):
		self.value = value
		self.dto_type = dto_type
		self.timestamp = timestamp
	
	def get(self):
		return self.value
	
	def getValue(self):
		return self.get()
		
	def getType(self):
		return self.dto_type
	
	def getTimestamp(self):
		return self.timestamp
