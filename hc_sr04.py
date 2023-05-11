#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
#  Filename: hc_sr04.py
#
#  Description: Simple class to interact with the HC-SR04 Ranging Sensor. The
#             main command to use is the calc_distance() function. All other
#             class functions support this function.
#
#  Author: Greg Kraus, gkraus@luf.co
#
#  History:
#    20230507 - initial creation
#
#-------------------------------------------------------------------------------

import os
import sys
import time
import RPi.GPIO as GPIO

class HC_SR04:
  def __init__(self, trig_pin, echo_pin):
    self.trig_pin = trig_pin
    self.echo_pin = echo_pin

    # GPIO.setmode(GPIO.BCM) # This should be set in main python module at init time
    GPIO.setup(self.trig_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    time.sleep( 0.2 ) # allow device to initialize

#----------------------------------------------------------

  def __del__(self):
    GPIO.cleanup( self.echo_pin )
    GPIO.cleanup( self.trig_pin )

#----------------------------------------------------------

  def get_echo(self):
    # reset echo measurement times
    echo_start = 0
    echo_stop = 0

    # make sure ECHO_PIN is LOW before starting
    self.gpio_wait_until( self.echo_pin, GPIO.LOW, 0.5)

    # issue trigger pulse (10 microseconds)
    GPIO.output(self.trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(self.trig_pin, GPIO.LOW)

    # look for echo pulse to START
    self.gpio_wait_until( self.echo_pin, GPIO.HIGH, 0.5)
    echo_start = time.monotonic_ns()

    # look for echo pulse to STOP
    self.gpio_wait_until( self.echo_pin, GPIO.LOW, 0.5)
    echo_stop = time.monotonic_ns()

    # check for timeouts
    if echo_stop == -1 or echo_start == -1:
      return -1 # no valid reading obtained

    return echo_stop - echo_start # echo pulse duration in nanoseconds

#----------------------------------------------------------
  
  def gpio_wait_until( self, pin, state, time_to_wait):
    timeout = time.monotonic_ns() + time_to_wait * 1e9
    while time.monotonic_ns() < timeout: 

      # only check for timeout 0.1% of the time - this
      # improves event detection time accuracy
      for ii in range(1000):
        if GPIO.input(pin) == state:
          return True # condition has occurred

    return False # timeout - condition never occurred
  
#----------------------------------------------------------

  def calc_distance(self, temp_C=20):
    time_ns = 0
    num_echos = 10
    t_ns = []
    for ii in range(0, num_echos):
      t_ns.append( self.get_echo() )
      time.sleep(0.25)

    # throw out high and low readings, then calc average
    t_max = max(t_ns)
    t_min = min(t_ns)
    t_avg_ns = (sum(t_ns) - t_max - t_min) / (num_echos - 2)
    
    # we want the one-way time, not the round-trip time
    t_one_way = t_avg_ns / 2

    # calculate distance based on speed of sound at given temp
    d_m = t_one_way * self.speed_of_sound( temp_C ) * 1e-9

    return d_m * 100   # return distance in centimeters 
  
#----------------------------------------------------------

  def speed_of_sound( self, temp_C=20 ):
    # calculate the speed of sound (m/s) for a given temperature 
    # between 0 - 100 Celcius
    # Speed of sound at 0 Celcius = 331 meters per second
    if temp_C > 100:
      t = 100
    elif temp_C < 0:
      t = 0
    else:
      t = temp_C

    return 331 + (0.6 * t)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
  print('HC-SR04 ultrasonic distance sensor - class test example')
  GPIO.setmode(GPIO.BCM)  # use BCM pin numbers

  TRIG_PIN = 23
  ECHO_PIN = 24
  sensor = HC_SR04(TRIG_PIN, ECHO_PIN)

  try:
    while True:
      d_cm = sensor.calc_distance()
      print('Distance to object: ' + '{:.2f}'.format(d_cm))
      time.sleep(0.5)
  except KeyboardInterrupt:
    pass
