#!/usr/bin/python3
#btntest.py
import time
import os
import RPi.GPIO as GPIO
#HARDWARE SETUP
# P1
# 2[==X==1=======]26
# 1[=============]25
#Button Config
BTN = 12

def gpio_setup():
  #Setup the wiring
  GPIO.setmode(GPIO.BOARD)
  #Setup Ports
  GPIO.setup(BTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
  

def main():
  gpio_setup()
  count=0
  btn_closed = True
  while True:
    btn_val = GPIO.input(BTN)
    if btn_val and btn_closed:
       print("OPEN")
       btn_closed=False
    elif btn_val==False and btn_closed==False:
       count+=1
       print("CLOSE %s" % count)
       os.system("flite -t '%s'" % count)
       btn_closed=True
    time.sleep(0.1)

try:
  main()
finally:
  GPIO.cleanup()
  print("Closed Everything. END")
#End
