#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15


ADS1115 = 0x01	# 16-bit ADC

adc = ADS1x15(ic=ADS1115)

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        adc.stopContinuousConversion()
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

adc.startContinuousConversion(0, 1024, 860)


list = []
calibration_factor = 0.78242

while True:

	max = 0.0
	min = 0.0
	
	amostras = 30
	t = 0

	while t < amostras:
		
		# V2 = I2 x R2
		# I2 = V2 / R2		
		# I1 = I2 x Turns
		# Turns = 1800
		# R2 = 62 Ohm
		Is = 0
		Vs = abs(adc.getLastConversionResults()/1000.0)
		if Vs > 0:
			Is = Vs/62
		Ip = 1800 * Is
		Vp = 230
		Wp = Ip * Vp

		Wp = Wp * calibration_factor
		#print Vs, Is, Ip, Wp
		if Wp > max:
			max = Wp
		t += 1
		time.sleep(0.5/amostras)

	if len(list) == 2:
		sum = 0.0
		for x in list:
			sum += x
		print "%.2d W/n" % (sum/len(list))
		list = []
	else:
		list.append(max)

adc.stopContinuousConversion()
