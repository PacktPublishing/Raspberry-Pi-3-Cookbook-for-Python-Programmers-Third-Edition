#!/usr/bin/env python3
import time
import wiringpi2
ON=1;OFF=0
IN=0;OUT=1
STEP=0.2
PINS=[15,16,18,22]   # PINS=[L_FWD,L_BWD,R_FWD,R_BWD]
FWD=[ON,OFF,ON,OFF]
BWD=[OFF,ON,OFF,ON]
RIGHT=[OFF,ON,ON,OFF]
LEFT=[ON,OFF,OFF,ON]
IO_ADDR=0x20
DEBUG=True

class motor:
  # Constructor
  def __init__(self,pins=PINS,steptime=STEP,pinbase=0,ADDR=IO_ADDR):
    self.pins=[]
    for p in pins:
      self.pins.append(p+pinbase)
    self.steptime=steptime
    self.GPIOsetup(pinbase)

  def GPIOsetup(self,pinbase=0,ADDR=IO_ADDR):
    wiringpi2.wiringPiSetupPhys()
    if (pinbase!=0):
      wiringpi2.mcp23017Setup(pinbase,ADDR)
    for gpio in self.pins:
      wiringpi2.pinMode(gpio,OUT)

  def off(self):
    for gpio in self.pins:
      wiringpi2.digitalWrite(gpio,OFF)

  def drive(self,drive,step=STEP):
    for idx,gpio in enumerate(self.pins):
      wiringpi2.digitalWrite(gpio,drive[idx])
      if(DEBUG):print("%s:%s"%(gpio,drive[idx]))
    time.sleep(step)
    self.off()

  def cmd(self,char,step=STEP):
    if char == 'f':
      self.drive(FWD,step)
    elif char == 'b':
      self.drive(BWD,step)
    elif char == 'r':
      self.drive(RIGHT,step)
    elif char == 'l':
      self.drive(LEFT,step)
    elif char == '#':
      time.sleep(step)

def main():
  import os
  if "CMD" in os.environ:
    CMD=os.environ["CMD"]
    INPUT=False
    print("CMD="+CMD)
  else:
    INPUT=True
  roverPi=motor(pins=[0,1,2,3],pinbase=100)
  if INPUT:
    print("Enter CMDs [f,b,r,l,#]:")
    CMD=input()
  for idx,char in enumerate(CMD.lower()):
    print("Step %s of %s: %s"%(idx+1,len(CMD),char))
    roverPi.cmd(char)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End

