#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import os

# Shutdown Script
DEBUG=False
SNDON=True
#HARDWARE SETUP
# P1
# 2[==X==L=======]26
# 1[===1=2=======]25
#BTN CONFIG - Set GPIO Ports
GPIO_MODE=GPIO.BOARD
SHTDWN_BTN = 7 #1
LAN_SW = 11    #2
LED = 12       #L


def gpio_setup():
  #Setup the wiring
  GPIO.setmode(GPIO_MODE)
  #Setup Ports
  GPIO.setup(SHTDWN_BTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
  GPIO.setup(LAN_SWA,GPIO.IN,pull_up_down=GPIO.PUD_UP)
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
    if(SNDON):os.system("flite -t 'Warning commencing power down in 3 2 1'")
    if(DEBUG==False):os.system("sudo shutdown -h now")
    if(DEBUG):GPIO.cleanup()
    if(DEBUG):exit()

def doChangeLAN(direct):
  if(DEBUG):print("Direct LAN: %s" % direct)
  if GPIO.input(LAN_SWA) and direct==True:
    if(DEBUG):print("LAN Switch OFF")
    cmd="sudo dhclient eth0"
    direct=False
    GPIO.output(LED,1)
  elif GPIO.input(LAN_SWA)==False and direct==False:
    if(DEBUG):print("LAN Switch ON")
    cmd="sudo ifconfig eth0 169.254.69.69"
    direct=True
  else:
    return direct
  os.system(cmd)
  if(SNDON):os.system("hostname -I | flite")
  return direct

def flashled(ledon):
  if ledon:
    ledon=False
  else:
    ledon=True
  GPIO.output(LED,ledon)
  return ledOn

def main():
  gpio_setup()
  GPIO.output(LED,1)
  directlan=False
  ledon=True
  while True:
    if(DEBUG):print("Waiting for >3sec button press")
    if GPIO.input(SHTDWN_BTN)==False:
       doShutdown()
    directlan = doChangeLAN(directlan)
    if directlan:
      flashled(ledon)
    time.sleep(1)

try:
  main()
finally:
  GPIO.cleanup()
  print("Closed Everything. END")
#End
