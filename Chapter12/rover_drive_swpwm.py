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
PWM_PIN_ENA=7;PWM_PIN_ENA=11;RANGE=100 #0-100 (100Hz Max)
ON_TIME1=20; ON_TIME2=75 #0-100
DEBUG=True

class motor:
  # Constructor
  def __init__(self,pins=PINS,steptime=STEP):
    self.pins = pins
    self.steptime=steptime
    self.GPIOsetup()

  def GPIOsetup(self):
    wiringpi2.wiringPiSetupPhys()
    wiringpi2.softPwmCreate(PWM_PIN_ENA,ON_TIME1,RANGE)
    wiringpi2.softPwmCreate(PWM_PIN_ENB,ON_TIME2,RANGE)
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
  roverPi=motor()
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

