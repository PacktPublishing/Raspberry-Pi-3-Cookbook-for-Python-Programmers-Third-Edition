#!/usr/bin/env python3
#rover_drivefwd.py
#HARDWARE SETUP
# P1
# 2[==X====LR====]26[=======]40
# 1[=============]25[=======]39
import time
import wiringpi2
ON=1;OFF=0
IN=0;OUT=1
STEP=0.5
PINS=[16,18] # PINS=[L-motor,R-motor]
FWD=[ON,ON]
RIGHT=[ON,OFF]
LEFT=[OFF,ON]
DEBUG=True

class motor:
  # Constructor
  def __init__(self,pins=PINS,steptime=STEP):
    self.pins = pins
    self.steptime=steptime
    self.GPIOsetup()

  def GPIOsetup(self):
    wiringpi2.wiringPiSetupPhys()
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
  roverPi=motor()
  if INPUT:
    print("Enter CMDs [f,r,l,#]:")
    CMD=input()
  for idx,char in enumerate(CMD.lower()):
    if(DEBUG):print("Step %s of %s: %s"%(idx+1,len(CMD),char))
    roverPi.cmd(char)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End

