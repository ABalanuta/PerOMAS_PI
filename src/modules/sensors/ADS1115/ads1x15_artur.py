#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15


ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

adc = ADS1x15(ic=ADS1115)


def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        adc.stopContinuousConversion()
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'



adc.startContinuousConversion(0, 1024, 860)





# Read channel 0 in single-ended mode using the settings above
#volts = adc.readADCSingleEnded(0, gain, sps) / 1000

# To read channel 3 in single-ended mode, +/- 1.024V, 860 sps use:
# volts = adc.readADCSingleEnded(3, 1024, 860)


ratio = 5.0

while True:

	max = 0.0

	amostras = 66
	t = 0

	while t < amostras:
		volts = adc.getLastConversionResults()
		#volts = int(adc.readADCSingleEnded(0, 1024, 860))
		if volts > max:
			max = volts
		#print int(volts)*ratio
		time.sleep(0.5/amostras) 
		t += 1
	print max*5

adc.stopContinuousConversion()
