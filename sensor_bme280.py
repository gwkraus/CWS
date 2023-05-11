#!/usr/bin/env python3

import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
# print(data.id)

print(str(data.timestamp).split('.')[0] + ' UTC')
print("Temp: {:.2f} ".format(data.temperature) + u'\xb0C')
print("Baro: {:.0f} ".format(data.pressure) + 'hPa')
print("Humi: {:.1f} ".format(data.humidity) + '%rH')

# there is a handy string representation too
# print(data)