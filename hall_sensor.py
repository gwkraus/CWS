#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
# Filename: hall_sensor.py
#
# Description: Simple class module to read status from a Raspberry Pi GPIO
#           pin. In this case a Hall Effect sensor is connected to the GPIO pin.
#           The logic sense of the pin is inverted, as a Hall effect sensor will
#           read as a 0 (LOW) on the GPIO pin when a magnet is near the sensor.
#
#           The parameter to create the class is:
#             * sensor_pin - this is the BCM GPIO pin number that the Hall Effect
#                         sensor is connected to.
#
#           For the initial test of this module, I used an A3141 sensor. The 
#           data sheet for this part is readily available on the Internet. There
#           are only 3 pins:
#               * Pin 1 - Power (must be >= 5V, and can be as high as 24 V)
#               * Pin 2 - Ground
#               * Pin 3 - Output (an open-collector output, which can sink a 
#                         fair amount of current).
#
#           Pin3 will be connected to the GPIO pin. Just be sure to configure 
#           the GPIO pin with the Pull-up feature enabled.  
#
# Author: Greg Kraus
# History: 20230512 Initial creation
#
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as GPIO

class HALL_SENSOR:
  def __init__( self, sensor_pin ):
    self.sensor_pin = sensor_pin
    GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  #------------------------------------

  def __del__(self):
    GPIO.cleanup( self.sensor_pin )

  #------------------------------------

  def __str__(self):
    state = self.state()
    return "Hall Sensor: {}".format("OFF" if state == GPIO.HIGH else "ON")
  
  #-------------------------------------
  
  def state( self ):
    return GPIO.input( self.sensor_pin )
    
#-------------------------------------------------------------------------------

if __name__ == '__main__':
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  HALL_PIN = 21
  sensor = HALL_SENSOR( HALL_PIN )
  
  try:
    while 1:
        print(sensor)
        time.sleep(1)
  except KeyboardInterrupt:
    pass
