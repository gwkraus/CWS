#!/usr/bin/env python3

#-------------------------------------------------------------------------------
#
#  Filename: logger.py
#
#  Description: Simple logging class module. Writes a timestampped message to a
#            specified log file.
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

class LOGGER:
  def __init__(self, filename):
    self.filename = filename
    try:
      if os.path.isfile(self.filename) == False:
        f = open(self.filename, "a")
        f.close()
    except FileNotFoundError:
      print("Error: Unable to open file " + self.filename + ". Exiting..." )
      sys.exit(255)

#---------------------------------------

  def __del__(self):
    pass

#---------------------------------------

  def write(self, msg):
    try:
      with open(self.filename, "a") as f:
        time_str = time.asctime()
        log_msg = time_str + ',' + msg + '\n'
        f.write(log_msg)
    except FileNotFoundError:
      print("Error: Unable to write log message to file " + self.filename + "." )

#---------------------------------------

if __name__ == "__main__":
  print('Logger class test example')
  filename = 'test_log.txt'

  log = LOGGER( filename )
  log.write('Just testing the LOGGER class')
  log.write('12,some stuff, some more stuff, the thing')