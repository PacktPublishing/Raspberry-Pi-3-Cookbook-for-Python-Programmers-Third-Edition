#!/usr/bin/env python3
#XLoBorg3-part1.py
import wiringpi2
import struct
import time

global DEBUG
DEBUG=False

def readBlockData(bus,device,register,words):
  magData=[]
  for i in range(words):
    magData.append(bus.readReg16(device,register+i))
  return magData

class compass:
  def __init__(self):
    addr = 0x0E #compass
    self.i2c = wiringpi2.I2C()
    self.devMAG=self.i2c.setup(addr)
    self.initCompass()

  def initCompass(self):
    # Acquisition mode
    register = 0x11   # CTRL_REG2
    data  = (1 << 7)  # Reset before each acquisition
    data |= (1 << 5)  # Raw mode, do not apply user offsets
    data |= (0 << 5)  # Disable reset cycle
    self.i2c.writeReg8(self.devMAG,register,data)
    # System operation
    register = 0x10   # CTRL_REG1
    data  = (0 << 5)  # Output data rate
                      # (10 Hz when paired with 128 oversample)
    data |= (3 << 3)  # Oversample of 128
    data |= (0 << 2)  # Disable fast read
    data |= (0 << 1)  # Continuous measurement
    data |= (1 << 0)  # Active mode
    self.i2c.writeReg8(self.devMAG,register,data)

  def readCompassRaw(self):
    #x, y, z = readCompassRaw()
    self.i2c.write(self.devMAG,0x00)
    [status, xh, xl, yh, yl,
     zh, zl, who, sm, oxh, oxl,
     oyh, oyl, ozh, ozl,
     temp, c1, c2] = readBlockData(self.i2c,self.devMAG, 0, 18)
    # Convert from unsigned to correctly signed values
    bytes = struct.pack('BBBBBB', xl, xh, yl, yh, zl, zh)
    x, y, z = struct.unpack('hhh', bytes)
    return x, y, z

if __name__ == '__main__':
  DEBUG=True
  myCompass=compass()
  try:
    while True:
      # Read the MAG Data
      mx, my, mz = myCompass.readCompassRaw()
      print ("mX = %+06d, mY = %+06d, mZ = %+06d" % (mx, my, mz))
      time.sleep(0.1)
  except KeyboardInterrupt:
    print("Finished")
#End
