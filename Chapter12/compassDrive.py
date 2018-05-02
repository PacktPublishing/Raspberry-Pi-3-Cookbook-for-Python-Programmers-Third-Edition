#!/usr/bin/env python3
#compassDrive.py
import XLoBorg3 as XLoBorg
import rover_drive as drive
import time

MARGIN=10 #turn until within 10degs
LEFT="l"; RIGHT="r"; DONE="#"

def calDir(target, current, margin=MARGIN):
  target=target%360
  current=current%360
  delta=(target-current)%360
  print("Target=%f Current=%f Delta=%f"%(target,current,delta))
  
  if delta <= margin:
    CMD=DONE
  else:
    if delta>180:
      CMD=LEFT
    else:
      CMD=RIGHT
  return CMD

def main():
  myCompass=XLoBorg.compass()
  myBot=drive.motor()
  while(True):
    print("Enter target angle:")
    ANGLE=input()
    try:
      angleTarget=float(ANGLE)
      CMD=LEFT
      while (CMD!=DONE):
        angleCompass=myCompass.readCompassAngle()
        CMD=calDir(angleTarget,angleCompass)
        print("CMD: %s"%CMD)
        time.sleep(1)
        myBot.cmd(CMD)
      print("Angle Reached!")
    except ValueError:
      print("Enter valid angle!")
      pass

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End
