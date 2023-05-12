#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
# Filename: bme280_sensor.py
#
# Description: Simple wrapper class to an existing BME280 python module. This
#           wrapper class provides some simplification of talking to the BME280.
#           Additionally it provides some convenience functions to retrieve the
#           sensor data and format the results.
#
#           To initialize the BME280, we need only to provide the I2C parameters
#           for the device. These are usually the defaults, and seldom change. 
#           The device address is usually 0x76 (or possibly 0x77). The port is 
#           almost always 1 (especially if it is a Raspberry Pi talking to the 
#           device.
#
# Author: Greg Kraus
# History: 20230512 Initial creation
#
#-------------------------------------------------------------------------------

import smbus2
import bme280

class BME280_WRAPPER:
  def __init__(self, addr=0x76, port=1):
    self.port = 1
    self.address = 0x76
  
    #open up a connection the I2C bus
    self.bus = smbus2.SMBus(port)

    # get calibration params from the device (makes for more accurate measurements)
    self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

  #-------------------------------------
  
  def __del__(self):
    pass
    
  #-------------------------------------
    
  def __str__(self):
    data = self.read()
    ss  = "Temp: {:.1f} ".format(data['temp']) + u'\xb0C' + '   '
    ss += "Baro: {:.0f} ".format(data['pressure']) + 'hPa   '
    ss += "Humidity: {:.1f} ".format(data['humidity']) + '%rH'
    return ss

  #-------------------------------------

  def read(self):
    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(self.bus, self.address, self.calibration_params)

    return {'temp':data.temperature, 'pressure':data.pressure, 'humidity': data.humidity}

#-------------------------------------------------------------------------------

if __name__ == '__main__':

  import time

  try:
    while 1:
      sensor = BME280_WRAPPER()
      print(sensor)
      time.sleep(1)
  except KeyboardInterrupt:
    pass
    
