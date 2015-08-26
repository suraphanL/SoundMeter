#!/usr/bin/env python

# Simple test script that plays (some) wav files


# Footnote: I'd normally use print instead of sys.std(out|err).write,
# but this version runs on python 2 and python 3 without conversion

import sys
import wave
import getopt
import alsaaudio
import audioop
import math
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4,GPIO.OUT)
#GPIO.setup(17,GPIO.OUT)
#GPIO.setup(27,GPIO.OUT)
#GPIO.setup(22,GPIO.OUT)
#GPIO.setup(18,GPIO.OUT)
#GPIO.setup(23,GPIO.OUT)
#GPIO.setup(24,GPIO.OUT)
#GPIO.setup(25,GPIO.OUT)

def play(device, f):    
    listPin = [4,17,27,22,18,23,24,15]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(27,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
	
    sys.stdout.write('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                                          f.getframerate()))
    # Set attributes
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    device.setperiodsize(320)
    lo  = 2000
    hi = 32000
 
    log_lo = math.log(lo)
    log_hi = math.log(hi)    
    data = f.readframes(320)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(320)
	vuTemp = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)/2
	vu = chr(ord('a')+min(max(int(vuTemp*20),0),19))
	print vu
    volume = 0
    
    if vu == 'd':
        volume = 1
    elif vu == 'e' :
        volume = 2
    elif vu == 'f' :
        volume = 3
    elif vu == 'g' :
        volume = 4
    elif vu == 'h' :
        volume = 5   
    elif vu == 'i' :
        volume = 6
    elif vu == 'j' :
        volume = 7
    elif vu == 'k' :
        volume = 8
    elif vu == 'l' :
        volume = 9
    else:
        volume = 0

    print volume

    for x in xrange(0,len(listPin)):
        GPIO.output(x,x<volume)
              
        
	# if vu == 'd':
	# 	GPIO.output(17,False)
 #                GPIO.output(4,False)
 #                GPIO.output(27,False)
 #                GPIO.output(22,False)
 #                GPIO.output(18,False)
 #                GPIO.output(23,False)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'e':
	# 	GPIO.output(4,True)
 #                GPIO.output(17,False)
 #                GPIO.output(27,False)
 #                GPIO.output(22,False)
 #                GPIO.output(18,False)
 #                GPIO.output(23,False)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'f':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,False)
 #                GPIO.output(22,False)
 #                GPIO.output(18,False)
 #                GPIO.output(23,False)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'g':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,False)
 #                GPIO.output(18,False)
 #                GPIO.output(23,True)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'h':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,True)
 #                GPIO.output(18,False)
 #                GPIO.output(23,False)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'i':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,True)
 #                GPIO.output(18,True)
 #                GPIO.output(23,False)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'j':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,True)
 #                GPIO.output(18,True)
 #                GPIO.output(23,True)
 #                GPIO.output(24,False)
 #                GPIO.output(25,False)
	# elif vu == 'k':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,True)
 #                GPIO.output(18,True)
 #                GPIO.output(23,True)
 #                GPIO.output(24,True)
 #                GPIO.output(25,False)
	# elif vu == 'i':
 #                GPIO.output(4,True)
 #                GPIO.output(17,True)
 #                GPIO.output(27,True)
 #                GPIO.output(22,True)
 #                GPIO.output(18,True)
 #                GPIO.output(23,True)
 #                GPIO.output(24,True)
 #                GPIO.output(25,True)
def usage():
    sys.stderr.write('usage: playwav.py [-c <card>] <file>\n')
    sys.exit(2)

if __name__ == '__main__':

    card = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    if not args:
        usage()
        
    f = wave.open(args[0], 'rb')
    device = alsaaudio.PCM(card=card)

    play(device, f)

    f.close()
