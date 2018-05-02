#!/usr/bin/python3
# socketControl.py
import time
import RPi.GPIO as GPIO
#HARDWARE SETUP
# P1
# 2[V=G====XI====]26[=======]40
# 1[=====321=====]25[=======]39
#V=5V  G=Gnd
sw_num=[15,13,11]#Pins for Switch 1,2,3
sw_state=[16,18]#Pins for State X=Off,I=On
MSGOFF=0; MSGON=1
SW_ACTIVE=0; SW_INACTIVE=1

class Switch():
  def __init__(self):
    self.setup()
  def __enter__(self):
    return self
  def setup(self):
    print("Do init")
    #Setup the wiring
    GPIO.setmode(GPIO.BOARD)
    for pin in sw_num:
      GPIO.setup(pin,GPIO.OUT)
    for pin in sw_state:
      GPIO.setup(pin,GPIO.OUT)
    self.clear()
  def message(self,number,state):
    print ("SEND SW_CMD: %s %d" % (number,state))
    if state==MSGON:
      self.on(number)
    else:
      self.off(number)
  def on(self,number):
    print ("ON: %d"% number)
    GPIO.output(sw_num[number-1],SW_ACTIVE)
    GPIO.output(sw_state[MSGON],SW_ACTIVE)
    GPIO.output(sw_state[MSGOFF],SW_INACTIVE)
    time.sleep(0.5)
    self.clear()
  def off(self,number):
    print ("OFF: %d"% number)
    GPIO.output(sw_num[number-1],SW_ACTIVE)
    GPIO.output(sw_state[MSGON],SW_INACTIVE)
    GPIO.output(sw_state[MSGOFF],SW_ACTIVE)
    time.sleep(0.5)
    self.clear()
  def clear(self):
    for pin in sw_num:
      GPIO.output(pin,SW_INACTIVE)
    for pin in sw_state:
      GPIO.output(pin,SW_INACTIVE)
  def __exit__(self, type, value, traceback):
    self.clear()
    GPIO.cleanup()

def main():
  with Switch() as mySwitches:
    mySwitches.on(1)
    time.sleep(5)
    mySwitches.off(1)  
    
if __name__ == "__main__":
    main()
#End
