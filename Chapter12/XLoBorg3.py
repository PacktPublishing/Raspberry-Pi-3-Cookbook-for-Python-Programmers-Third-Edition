#!/usr/bin/env python3
#XLoBorg3.py
import wiringpi2
import struct
import time
import math

CAL=100 #take CAL samples
FILENAME="mag.cal"
global DEBUG
DEBUG=False

def readBlockData(bus,device,register,words):
  magData=[]
  for i in range(words):
    magData.append(bus.readReg16(device,register+i))
  return magData

class compass:
  def __init__(self,newCal=False):
    addr = 0x0E #compass
    self.i2c = wiringpi2.I2C()
    self.devMAG=self.i2c.setup(addr)
    self.initCompass()
    self.offset,self.scaling=self.readCal(newCal)
    if DEBUG:print("offset:%s scaling:%s"%(str(self.offset),
                                           str(self.scaling)))

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

  def readCal(self,newCal=False,filename=FILENAME):
    if newCal==False:
      try:
        with open(FILENAME,'r') as magCalFile:
          line=magCalFile.readline()
          offset=line.split()
          line=magCalFile.readline()
          scaling=line.split()
          if len(offset)==0 or len(scaling)==0:
            raise ValueError()
          else:
            offset=list(map(float, offset))
            scaling=list(map(float, scaling))
      except (OSError,IOError,TypeError,ValueError) as e:
        print("No Cal Data")
        newCal=True
        pass
    if newCal==True:
      print("Perform New Calibration")
      offset,scaling=self.calibrateCompass()
      self.writeCal(offset,scaling)
    return offset,scaling
  
  def writeCal(self,offset,scaling):
      if DEBUG:print("Write Calibration")
      if DEBUG:print("offset:"+str(offset))
      if DEBUG:print("scaling:"+str(scaling))
      with open(FILENAME,'w') as magCalFile:
        for value in offset:
          magCalFile.write(str(value)+" ")
        magCalFile.write("\n")
        for value in scaling:
          magCalFile.write(str(value)+" ")
        magCalFile.write("\n")
  
  def calibrateCompass(self,samples=CAL):
    MAXS16=32768
    SCALE=1000.0
    avg=[0,0,0]
    min=[MAXS16,MAXS16,MAXS16];max=[-MAXS16,-MAXS16,-MAXS16]
    print("Move sensor around axis (start in 5 sec)")
    time.sleep(5)
    for calibrate in range(samples):
      for idx,value in enumerate(self.readCompassRaw()):
        avg[idx]+=value
        avg[idx]/=2
        if(value>max[idx]):
          max[idx]=value
        if(value<min[idx]):
          min[idx]=value
      time.sleep(0.1)
      if DEBUG:print("#%d min=[%+06d,%+06d,%+06d]"
                     %(calibrate,min[0],min[1],min[2])
                     +" avg[%+06d,%+06d,%+06d]"
                     %(avg[0],avg[1],avg[2])
                     +" max=[%+06d,%+06d,%+06d]"
                     %(max[0],max[1],max[2]))
    offset=[]
    scaling=[]
    for idx, value in enumerate(min):
      magRange=max[idx]-min[idx]
      offset.append((magRange/2)+min[idx])
      scaling.append(SCALE/magRange)
    return offset,scaling

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

  def readCompass(self):
    raw = self.readCompassRaw()
    if DEBUG:print("mX = %+06d, mY = %+06d, mZ = %+06d"
                   % (raw[0],raw[1],raw[2]))
    read=[]
    for idx,value in enumerate(raw):
      adj=value-self.offset[idx]
      read.append(adj*self.scaling[idx])
    return read

  def readCompassAngle(self,cal=True):
    if cal==True:
      read = self.readCompass()
    else:
      read = self.readCompassRaw()
    angle = math.atan2 (read[1],read[0]) # cal angle in radians
    if (angle < 0):
      angle += (2 * math.pi) # ensure positive
    angle = (angle*360)/(2*math.pi); #report in degrees
    return angle

if __name__ == '__main__':
  DEBUG=True
  myCompass=compass()
  try:
    while True:
      # Read the MAG Data
      mx, my, mz = myCompass.readCompassRaw()
      print ("mX = %+06d, mY = %+06d, mZ = %+06d" % (mx, my, mz))
      print("Angle: %.2f"%(myCompass.readCompassAngle()))
      time.sleep(0.1)
  except KeyboardInterrupt:
    print("Finished")
#End
