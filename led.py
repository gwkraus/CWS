#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
# Filename: led.py
#
# Description: Simple class module to control an LED from a Raspberry Pi GPIO
#           pin. Class can be configured for any GPIO pin, as well as for how 
#           the LED is driven (source or sink mode). There are 2 basic functions
#           to control the LED: toggle() and set(). 
#
#           The parameters to create the class are:
#             * led_pin - this is the BCM GPIO pin number that the LED is 
#                         connected to
#             * isSink - a boolean value indicating if the GPIO pin is sourcing
#                         the LED with voltage or providing a ground to it.
#             * initial_state - what state you want the LED to be in when the
#                         object is created (0 = OFF, 1 = ON). isSink has no
#                         effect on this value.
#
#           If you have a choice, using sink mode to control the LED is a better 
#           choice in general. Most CPU pins can sink more current than they can
#           provide as a voltage source. Only if you are using an external 
#           transistor as a switch to control the LED should you use source mode.
#
# Author: Greg Kraus
# History: 20230512 Initial creation
#
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as GPIO

class LED:
  def __init__(self, led_pin, isSink=False, initial_state=0):
    GPIO.setup(led_pin, GPIO.OUT)
    self.led_pin = led_pin
    self.isSink = isSink
    self.led_state = initial_state
    self.update_pin()
    
  #-------------------------------------

  def __del__(self):
    GPIO.cleanup( self.led_pin )
    
  #-------------------------------------
  
  def __str__(self):
    return "LED: {}".format("OFF" if self.led_state == 0 else "ON")

  #-------------------------------------
  
  def toggle(self):
    self.led_state = 1 if self.led_state == 0 else 0
    self.update_pin()
    return self.led_state
  
  #-------------------------------------
  
  def set(self, state):
    self.led_pin = state
    self.update_pin()
    
  #-------------------------------------
    
  def update_pin(self):
    pin_state = self.led_state if self.isSink == False else not self.led_state
    GPIO.output(self.led_pin, pin_state)
    return self.led_state
    
#-------------------------------------------------------------------------------    
    
if __name__ == '__main__':
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  LED_PIN = 25
  led = LED( LED_PIN, True )
  
  try:
    while 1:       
      led.toggle()
      print(led)
      time.sleep(0.05)
      led.toggle()
      print(led)
      time.sleep(1.95)
  except KeyboardInterrupt:
    pass
    
