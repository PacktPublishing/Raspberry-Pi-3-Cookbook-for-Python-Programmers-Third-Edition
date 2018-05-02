#!/usr/bin/python3
#ledtest.py
import time
import RPi.GPIO as GPIO
# RGB LED module
#HARDWARE SETUP
# P1
# 2[======XRG=B==]26
# 1[=============]25
# X=GND R=Red G=Green B=Blue

#Setup Active States
#Common Cathode RGB-LED (Cathode=Active Low)
RGB_ENABLE = 1; RGB_DISABLE = 0

#LED CONFIG - Set GPIO Ports
RGB_RED = 16; RGB_GREEN = 18; RGB_BLUE = 22
RGB = [RGB_RED,RGB_GREEN,RGB_BLUE]

def led_setup():
  #Setup the wiring
  GPIO.setmode(GPIO.BOARD)
  #Setup Ports
  for val in RGB:
    GPIO.setup(val,GPIO.OUT)

def main():
  led_setup()
  for val in RGB:
    GPIO.output(val,RGB_ENABLE)
    print("LED ON")
    time.sleep(5)
    GPIO.output(val,RGB_DISABLE)
    print("LED OFF")

try:
  main()
finally:
  GPIO.cleanup()
  print("Closed Everything. END")
#End
