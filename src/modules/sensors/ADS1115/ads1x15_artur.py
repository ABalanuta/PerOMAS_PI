#!/usr/bin/env python
"""Consumption Estimation

Uses the ADS1115 Adafruit lib to estimate the values read by the ADC to
Real power consumption in Watts.
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import time, signal, sys
import numpy
from Adafruit_ADS1x15 import ADS1x15


ADS1115 = 0x01	# 16-bit ADC

adc = ADS1x15(ic=ADS1115)

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        adc.stopContinuousConversion()
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

#reads values +-1V with 860 samples/s
adc.startContinuousConversion(0, 1024, 860)


list = []
calibration_factor = 1.1

media = 0

while True:

	max = 0.0
	min = 0.0
	
	amostras = 120
	t = 0

	while t < amostras:
		
		# V2 = I2 x R2
		# I2 = V2 / R2		
		# I1 = I2 x Turns
		# Turns = 1800
		# R2 = 62 Ohm
		Is = 0
		Vs = adc.getLastConversionResults()/1000.0
		if Vs != 0:
			Is = Vs/182
		Ip = 1800 * Is
		Vp = 230
		Wp = Ip * Vp
	
		list.append(Wp)
		
		print Wp
		#print Vs, Is, Ip, Wp
		t += 1
		time.sleep(1/amostras)
		
	print numpy.mean(list)
	list = []
	#if len(list) == 4:
	#	sum = 0.0
	#	for x in list:
	#		sum += x
	#	print "%.1f" % (sum/len(list)), "W"
	#	list = []
	#else:
	#	list.append(max)

adc.stopContinuousConversion()
