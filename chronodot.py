#!/usr/bin/python3

#-------------------------------------------------------------------------------
#
# Filename: chronodot.py
#
# Description: A simple class that will communicate with the Chonodot. This
#           module only support setting and getting date-and-time on the 
#           chronodot module. The time is always 24 hour format, and day of
#           week is not supported. No alarm functions are supported.
#
#           If you call str() on the instantiated class object, you will
#           get a nice YYYY-MM-DD HH:mm:SS formatted string of the current
#           date and time.
#
# Author: Greg Kraus
#
# History: 20230510 Initial version
#
#-------------------------------------------------------------------------------

import time
from smbus2 import SMBus

# register order - from DS3231 Data Sheet
ds3231_reg = {
  'sec'    : 0,
  'min'    : 1,
  'hour'   : 2,
  'dow'    : 3,
  'day'    : 4,
  'month'  : 5,
  'year'   : 6,
  'ctrl'   : 14,
  'status' : 15
}

class DS3231:
  def __init__(self, i2c_addr = 0x68, bus_id = 1):
    self.i2c_addr = i2c_addr
    self.bus = SMBus(bus_id)
    # write control register to disable alarms and Squarewave output
    self.bus.write_byte_data(self.i2c_addr, ds3231_reg['ctrl'], 0)

  #-----------------------------------------

  def __del__(self):
    pass
      
  #-----------------------------------------

  def __str__(self):
    data = self.get_date_time()
    s =  "{:4n}-".format(2000 + data[ds3231_reg['year']])
    s += "{:02n}-".format(data[ds3231_reg['month']])
    s += "{:02n} ".format(data[ds3231_reg['day']])
    s += "{:02n}:".format(data[ds3231_reg['hour']])
    s += "{:02n}:".format(data[ds3231_reg['min']])
    s += "{:02n}".format(data[ds3231_reg['sec']])
    return s

  #-----------------------------------------

  def set_date_time(self, data):
      # convert to bcd format
      data[ds3231_reg['year']] -= 2000  # remove century from year
      data[ds3231_reg['dow']] += 1  # adjust day of week (per data sheet)       
      reg_data = [self.BinaryToBCD(x) for x in data]
      # print( reg_data )
      # write bcd data to DS3231
      self.bus.write_i2c_block_data(self.i2c_addr, 0, reg_data)
    
  #-----------------------------------------

  def get_date_time(self):
      # read bcd data from DS3231
      reg_data = self.bus.read_i2c_block_data(self.i2c_addr, 0, 7)
      # print( reg_data )
      reg_data[ds3231_reg['hour']] &= 0x3F  # mask off 12/24 hr bit
      reg_data[ds3231_reg['month']] &= 0x1F # mask off century bit
      reg_data[ds3231_reg['dow']] -= 1  # limit day of week        
      # convert to bcd format
      data = [self.bcdToBinary(x) for x in reg_data]
      #print( data )
      return data

  #-----------------------------------------

  def bcdToBinary(self, data):
      return (data//16) * 10 + (data%16)
  #-----------------------------------------

  def BinaryToBCD(self, data):
      return (data//10) * 16 + (data%10)

#-------------------------------------------------------------------------------

if __name__ == '__main__':

  # create an RTC object
  rtc = DS3231()
  
  # get the time from the computer
  t = time.localtime()
  
  #re-order the time parameters to match the DS3231 RTC register order
  data = [ t.tm_sec, t.tm_min, t.tm_hour, t.tm_wday+1, t.tm_mday, t.tm_mon, t.tm_year ]
  try:
    # rtc.set_date_time( data )  # comment this out to see how well rtc syncs
                                 # with compter time over several days

    # run a loop printing out the time values from RTC and computer
    while( 1 ):
      print("time: " + time.ctime() )
      print("rtc: " + str(rtc))
      time.sleep( 2 )
  except KeyboardInterrupt:
    pass   # Ctrl-C to exit program
    
