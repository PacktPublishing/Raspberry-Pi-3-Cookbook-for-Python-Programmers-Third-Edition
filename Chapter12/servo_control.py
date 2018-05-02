#!/usr/bin/env python3
#servo_control.py
import curses
import os
#HARDWARE SETUP
# GPIO
# 2[=VX==2=======]26[=======]40
# 1[===013=======]25[=======]39
# V=5V X=Gnd
# Servo 0=Turn 1=Shoulder 2=Elbox 3=Claw
name=["Turn","Shoulder","Elbow","Claw"]
CAL=[90,90,90,90]
MIN=[0,60,40,60]; MAX=[180,165,180,180]
POS=list(CAL)
KEY_CMD=[ord('c'),ord('x')]
#Keys to rotate counter-clockwise
KEY_LESS={ord('d'):0,ord('s'):1,ord('j'):2,ord('k'):3}
#Keys to rotate clockwise
KEY_MORE={ord('a'):0,ord('w'):1,ord('l'):2,ord('i'):3}

STEP=5; LESS=-STEP; MORE=STEP #Define control steps
DEG2MS=8.3333; OFFSET=1000 #mseconds
IDLE=2000 #Timeout servo after command
SERVOD="/home/pi/PiBits/ServoBlaster/user/servod" #Location of servod
DEBUG=True
text="Use a-d, w-s, j-l and i-k to control the MeArm. c=Cal x=eXit"

def initalise():
  cmd=("sudo %s --idle-timeout=%s"%(SERVOD, IDLE))
  os.system(cmd)

def limitServo(servo,value):
  global text
  if value > MAX[servo]:
    text=("Max %s position %s:%s"%(name[servo],servo,POS[servo]))
    return MAX[servo]
  elif value < MIN[servo]:
    text=("Min %s position %s:%s"%(name[servo],servo,POS[servo]))
    return MIN[servo]
  else:
    return value

def updateServo(servo,change):
  global text
  POS[servo]=limitServo(servo,POS[servo]+change)
  setServo(servo,POS[servo])
  text=str(POS)

def setServo(servo,position):
  ms=OFFSET+(position*DEG2MS)
  os.system("echo %d=%dus > /dev/servoblaster" %(servo,ms))

def calibrate():
  global text
  text="Calibrate 90deg"
  for i,value in enumerate(CAL):
    POS[i]=value
    setServo(i,value)

def main(term):
  term.nodelay(1)
  term.addstr(text)
  term.refresh()
  while True:
    term.move(1,0)
    c = term.getch()
    if c != -1:
      if c in KEY_MORE:
        updateServo(KEY_MORE[c],MORE)
      elif c in KEY_LESS:
        updateServo(KEY_LESS[c],LESS)
      elif c in KEY_CMD:
        if c == ord('c'):
          calibrate()
        elif c == ord('x'):
          exit()
      if DEBUG:term.addstr(text+"   ")

if __name__=='__main__':
  initalise()
  curses.wrapper(main)
#End
