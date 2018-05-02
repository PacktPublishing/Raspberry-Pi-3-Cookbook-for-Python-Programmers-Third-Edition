#!/usr/bin/env python3
#bug_drive.py
import time
import servoAdafruit as servoCon

servoMin = 205  # Min pulse 1000us 204.8 (50Hz)
servoMax = 410  # Max pulse 2000us 409.6 (50Hz)

servoL=0; servoM=1; servoR=2
TILT=20
MOVE=30
MID=((servoMax-servoMin)/2)+servoMin
CW=MID+MOVE; ACW=MID-MOVE
TR=MID+TILT; TL=MID-TILT
FWD=[TL,ACW,ACW,TR,CW,CW]#[midL,fwd,fwd,midR,bwd,bwd]
BWD=[TR,ACW,ACW,TL,CW,CW]#[midR,fwd,fwd,midL,bwd,bwd]
LEFT=[TR,ACW,CW,TL,CW,ACW]#[midR,fwd,bwd,midL,bwd,fwd]
RIGHT=[TL,ACW,CW,TR,CW,ACW]#[midL,fwd,bwd,midR,bwd,fwd]
HOME=[MID,MID,MID,MID,MID,MID]
PINS=[servoM,servoL,servoR,servoM,servoL,servoR]    
STEP=0.2
SPEED=0.1

global DEBUG
#DEBUG=False
DEBUG=True

class motor:
  # Constructor
  def __init__(self,pins=PINS,steptime=STEP):
    self.pins = pins
    self.steptime=steptime
    self.theServo=servoCon.servo()
  
  def off(self):
    #Home position
    self.drive(HOME,step)

  def drive(self,drive,step=STEP):
    for idx,servo in enumerate(self.pins):
      if(drive[idx]==servoM):
        time.sleep(step)
      self.theServo.setPWM(servo,0,drive[idx])
      if(drive[idx]==servoM):
        time.sleep(step)
      if(DEBUG):print("%s:%s"%(servo,drive[idx]))
      time.sleep(SPEED)

  def cmd(self,char,step=STEP):
    if char == 'f':
      self.drive(FWD,step)
    elif char == 'b':
      self.drive(BWD,step)
    elif char == 'r':
      self.drive(RIGHT,step)
    elif char == 'l':
      self.drive(LEFT,step)
    elif char == 'h':
      self.drive(HOME,step)
    elif char == '#':
      time.sleep(step)

def main():
  import os
  DEBUG=True
  if "CMD" in os.environ:
    CMD=os.environ["CMD"]
    INPUT=False
    print("CMD="+CMD)
  else:
    INPUT=True
  bugPi=motor()
  if INPUT:
    print("Enter CMDs [f,b,r,l,h,#]:")
    CMD=input()
  for idx,char in enumerate(CMD.lower()):
    if(DEBUG):print("Step %s of %s: %s"%(idx+1,len(CMD),char))
    bugPi.cmd(char)
  
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End

