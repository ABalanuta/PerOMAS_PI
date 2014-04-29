#!/usr/bin/python

import time
import math
from Adafruit_I2C import Adafruit_I2C

# ============================================================================
# Adafruit PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class HTU21D :
	
	i2c = None
	
	# Address of the device
	ADDR = 0x40
		
	# Registers/etc.
	CMD_READ_TEMP_HOLD = 0xe3
	CMD_READ_HUM_HOLD = 0xe5
	CMD_READ_TEMP_NOHOLD = 0xf3
	CMD_READ_HUM_NOHOLD = 0xf5
	CMD_WRITE_USER_REG = 0xe6
	CMD_READ_USER_REG = 0xe7
	CMD_SOFT_RESET= 0xfe
	
	def __init__(self, debug=False):
		
		self.i2c = Adafruit_I2C(self.ADDR)
		self.debug = debug
		
		if (self.debug):
			print "Reseting HTU21D"
		self.i2c.write8(self.ADDR, self.CMD_SOFT_RESET)
		time.sleep(.02)



h = HTU21D()
