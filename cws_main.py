#!/usr/bin/env python3

import RPi.GPIO as GPIO
import chronodot as cdot
import hall_sensor as hall
import hc_sr04 as ranger
import logger

WATER_OUT_PIN = 11111
RANGE_TRIGGER_PIN = 22222
RANGE_ECHO_PIN = 33333

logfile_name = 'cws_log.txt'
log = logger(logfile_name)

rtc = cdot.DS3231()
temp_sensor = temp.bmp280()
water_out = hall.hall_sensor(WATER_OUT_PIN)
range_sensor = ranger.HC_SR04(RANGE_TRIGGER_PIN, RANGE_ECHO_PIN)

WATER_LEVEL_FULL = 111.222   # range measurement from sensor to full water level
WATER_LEVEL_EMPTY = 333.444  # range measurement from sensor to WATER_OUT_LEVEL
NUMBER_OF_BUCKETS = 2
BUCKET_RADIUS = 11.22

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

set_interval_alarm()
while 1:

  wait_for_interval_alarm()

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

