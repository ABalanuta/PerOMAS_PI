#!/usr/bin/python

#import smbus
#import time

#bus = smbus.SMBus(1)

#define HTDU21D_ADDRESS 0x40  //Unshifted 7-bit I2C address for the sensor
#define TRIGGER_TEMP_MEASURE_HOLD  0xE3
#define TRIGGER_HUMD_MEASURE_HOLD  0xE5
#define TRIGGER_TEMP_MEASURE_NOHOLD  0xF3
#define TRIGGER_HUMD_MEASURE_NOHOLD  0xF5
#define WRITE_USER_REG  0xE6
#define READ_USER_REG  0xE7
#define SOFT_RESET  0xFE

#while True:
#
#   for a in range(0,4):
#      bus.write_byte_data(0x48,0x40 | ((a+1) & 0x03), 0)
#      v = bus.read_byte(0x48)
#      print v,
#      time.sleep(0.1)
#
#   print


#!/usr/bin/python

import time
from Adafruit_I2C import Adafruit_I2C
import binascii
# ===========================================================================
# HTU21D Class
# ===========================================================================

class HTU21D:

	i2c = None
	
	#Variables
	BUS							= 0
	DEBUG						= True

	# HTU21D Address
	address 					= 0x40
	
	# Commands
	TRIGGER_TEMP_MEASURE_HOLD	= 0xE3
	TRIGGER_HUMD_MEASURE_HOLD	= 0xE5
	READ_USER_REG = 0xE7

	# Constructor
	def __init__(self):
		self.i2c = Adafruit_I2C(self.address, self.BUS, self.DEBUG)
		
	def readUserRegister(self):
		"Read the user register byte"
		return self.i2c.readU8(self.READ_USER_REG)
	
	def readTemperatureData(self):
		"Read 3 temperature bytes from the sensor"
		# value[0], value[1]: Raw temperature data
		# value[2]: CRC
		value = 127
		value = self.i2c.readList(self.TRIGGER_TEMP_MEASURE_HOLD, 3)
		print value
		
		# CRC Check
		if not self.crc8check(value):
			return -255
			
		rawTempData = ( value[0] << 8 ) + value[1]
		
		# Clear the status bits
		rawTempData = rawTempData & 0xFFFC;
		
		# Calculate the actual temperature
		actualTemp = -46.85 + (175.72 * rawTempData / 65536)
		
		return actualTemp

	def readHumidityData(self):
		"Read 3 humidity bytes from the sensor"
		# value[0], value[1]: Raw relative humidity data
		# value[2]: CRC
		value = self.i2c.readList(self.TRIGGER_HUMD_MEASURE_HOLD, 3)
		
		# CRC Check
		if not self.crc8check(value):
			return -255

		rawRHData = ( value[0] << 8 ) + value[1]
		
		# Clear the status bits
		rawRHData = rawRHData & 0xFFFC;
		
		# Calculate the actual RH
		actualRH = -6 + (125.0 * rawRHData / 65536)
		
		return actualRH
	
	def crc8check(self, value):
		"Calulate the CRC8 for the data received"
		# Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
		remainder = ( ( value[0] << 8 ) + value[1] ) << 8
		remainder |= value[2]
		
		# POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
		# divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
		divsor = 0x988000
		
		for i in range(0, 16):
			if( remainder & 1 << (23 - i) ):
				remainder ^= divsor

			divsor = divsor >> 1
		
		if remainder == 0:
			return True
		else:
			return False
	

t = HTU21D()

#print t.readUserRegister()
print t.readHumidityData()
