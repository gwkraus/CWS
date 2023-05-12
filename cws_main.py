#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
# Filename: cws_main.py
#
# Description: This is the main project file for the Chicken Watering System 
#           (CWS) Stem project. The objectives of this project are:
#           * monitor the water volume remaining in the system
#           * provide an alert when the remaining water volume becomes critically
#             low
#           * provide alerts when the temperature of the CWS environment becomes
#             excessively hot or cold
#           * provide metrics about water consumption rate over time
#           * estimate time of next 'water critically low' event
#           * provide historical water refill times and amounts
#           * provide a user interface that will display current system status 
#             refill data, and graph of water consumption over time
#
# Author: Greg Kraus
#
# History:  20230512 Initial work started
#
#-------------------------------------------------------------------------------

import os
import sys
import time

import RPi.GPIO as GPIO
from chronodot import DS3231
from hall_sensor import HALL_SENSOR
from hc_sr04 import HC_SR04
from bme28_sensor import BME280_WRAPPER
from logger import LOGGER

# Configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # use BCM pin numbers

# Create system sensor objects

rtc = DS3231()
temp_sensor = BME280_WRAPPER

RANGE_TRIGGER_PIN = 23
RANGE_ECHO_PIN = 24
ranger = HC_SR04(RANGE_TRIGGER_PIN)

LED_PIN = 25
status_led = LED(LED_PIN)

HALL_SENSOR_PIN = 21
water_out_sensor = HALL_SENSOR(HALL_SENSOR_PIN)

# initialize logging
logfile_name = 'cws_log.txt'
log = logger(logfile_name)

# set some system parameters
MEASUREMENT_INTERVAL_MINUTES  5

WATER_LEVEL_FULL_DISTANCE = 111.222   # range measurement from sensor to full water level
WATER_LEVEL_EMPTY_DISTANCE = 333.444  # range measurement from sensor to WATER_OUT_LEVEL
NUMBER_OF_WATER_BUCKETS = 2
BUCKET_CAPACITY_LITERS = 5 * 3.875
BUCKET_RADIUS_CM = 1234

# Calulate the system's total water capacity
# volume = height * (pi * r^2)
# water has a volume of 231 cubic inches per gallon
# water has a volume of 1000 cubic centimeters per liter
# 1 gal of water = 3.875 liter
# 5 gal = 19.375 liters

# Keep historical average consumption rate of water
# weight previous 24 hrs consumption heavier than prior day's rate.
# keep updated "empty time prediction" based on each updated reading
# plot 'capacity versus time' for previous week

status = {}

# create initial display

while 1:
  # update system status
  
  # write system status to database
  
  # update display
  
  # go into sleep mode until next update is needed
  next_update_timestamp = ts_monotonic() + (MEASUREMENT_INVERVAL+_MINUTES * 60)
  
  while next_update_timestamp > ts_monotonic():
    status_led.toggle()
    time.sleep(0.05)
    status_led.toggle()
    time_sleep(1.95)
    

#-------------------------------------------------------------------------------
# Initial thoughts and todo list while prototyping

  update_display_alarm(water_out.get_sensor_state())
  tempC = temp_sensor.get_temp_celcius()
  dist_cm = range_sensor.get_level(tempC)

  water_volume_remaining = calc_water_volume( dist_cm, WATER_LEVEL_EMPTY, BUCKET_RADIUS)
  pct_full = (water_volume_remaining / max_water_volume) * 100

  # write reading to log file
  # first, get last log entry and compare to current reading
  # if level and temp are unchanged, just update timestamp
  # if level and/or temp are different, create new entry
  # logfile entry format:
  #     timestamp, tempC, level, volume_remaining, pct_full

  update_display( tempC, water_volume_remaining, pct_full )
  update_plot()

