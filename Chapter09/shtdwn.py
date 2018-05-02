#!/usr/bin/python3
#shtdown.py
import time
import RPi.GPIO as GPIO
import os

# Shutdown Script
DEBUG=False
SNDON=True
#HARDWARE SETUP
# P1
# 2[==X==L=======]26
# 1[===1=========]25
#BTN CONFIG - Set GPIO Ports
GPIO_MODE=GPIO.BOARD
SHTDWN_BTN = 7 #1
LED = 12       #L

def gpio_setup():
  #Setup the wiring
  GPIO.setmode(GPIO_MODE)
  #Setup Ports
  GPIO.setup(SHTDWN_BTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
  GPIO.setup(LED,GPIO.OUT)

def doShutdown():
  if(DEBUG):print("Press detected")
  time.sleep(3)
  if GPIO.input(SHTDWN_BTN):
    if(DEBUG):print("Ignore the shutdown (<3sec)")
  else:
    if(DEBUG):print ("Would shutdown the RPi Now")
    GPIO.output(LED,0)
    time.sleep(0.5)
    GPIO.output(LED,1)
    if(SNDON):os.system("flite -t 'Warning commencing power down'")
    if(DEBUG==False):os.system("sudo shutdown -h now")
    if(DEBUG):GPIO.cleanup()
    if(DEBUG):exit()

def main():
  gpio_setup()
  GPIO.output(LED,1)
  while True:
    if(DEBUG):print("Waiting for >3sec button press")
    if GPIO.input(SHTDWN_BTN)==False:
       doShutdown()
    time.sleep(1)

try:
  main()
finally:
  GPIO.cleanup()
  print("Closed Everything. END")
#End
