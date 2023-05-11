#!/usr/bin/env python3

import RPi.GPIO as GPIO

class hall_sensor:
  def __init__( self, sensor_pin ):
    self.sensor_pin = sensor_pin
    GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def __del__(self):
    GPIO.cleanup( self.sensor_pin )

  def get_sensor_state( self ):
    return GPIO.input( self.sensor )
