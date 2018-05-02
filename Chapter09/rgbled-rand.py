#!/usr/bin/python3
#rgbled-rand.py
import time
from random import randint
import RPi.GPIO as GPIO

#Setup Active states
#Common Cathode RGB-LEDs (Cathode=Active Low)
LED_ENABLE = 0; LED_DISABLE = 1
RGB_ENABLE = 1; RGB_DISABLE = 0
#HARDWARE SETUP
# P1
# 2[=====1=23=4==]26
# 1[===5=RGB=====]25
#LED CONFIG - Set GPIO Ports
LED1 = 12; LED2 = 16; LED3 = 18; LED4 = 22; LED5 = 7
LED = [LED1,LED2,LED3,LED4,LED5]
RGB_RED = 11; RGB_GREEN = 13; RGB_BLUE = 15
RGB = [RGB_RED,RGB_GREEN,RGB_BLUE]
#Mixed Colors
RGB_CYAN = [RGB_GREEN,RGB_BLUE]
RGB_MAGENTA = [RGB_RED,RGB_BLUE]
RGB_YELLOW = [RGB_RED,RGB_GREEN]
RGB_WHITE = [RGB_RED,RGB_GREEN,RGB_BLUE]
RGB_LIST = [RGB_RED,RGB_GREEN,RGB_BLUE,RGB_CYAN,
            RGB_MAGENTA,RGB_YELLOW,RGB_WHITE]

def led_setup():
  '''Setup the RGB-LED module pins and state.'''
  #Set up the wiring
  GPIO.setmode(GPIO.BOARD)
  # Setup Ports
  for val in LED:
    GPIO.setup(val, GPIO.OUT)
  for val in RGB:
    GPIO.setup(val, GPIO.OUT)
  led_clear()

def led_gpiocontrol(pins,state):
  '''This function will control the state of
  a single or multiple pins in a list.'''
  #determine if "pins" is a single integer or not
  if isinstance(pins,int):
    #Single integer - reference directly
    GPIO.output(pins,state)
  else:
    #if not, then cycle through the "pins" list
    for i in pins:
      GPIO.output(i,state)

def led_activate(led,color):
  '''Enable the selected led(s) and set the required color(s)
  Will accept single or multiple values'''
  #Enable led
  led_gpiocontrol(led,LED_ENABLE)
  #Enable color
  led_gpiocontrol(color,RGB_ENABLE)

def led_deactivate(led,color):
  '''Deactivate the selected led(s) and set the required
  color(s) will accept single or multiple values'''
  #Disable led
  led_gpiocontrol(led,LED_DISABLE)
  #Disable color
  led_gpiocontrol(color,RGB_DISABLE)
  
def led_time(led, color, timeon):
  '''Switch on the led and color for the timeon period'''
  led_activate(led,color)
  time.sleep(timeon)
  led_deactivate(led,color)

def led_clear():
  '''Set the pins to default state.'''
  for val in LED:
    GPIO.output(val, LED_DISABLE)
  for val in RGB:
    GPIO.output(val, RGB_DISABLE)

def led_cleanup():
  '''Reset pins to default state and release GPIO'''
  led_clear()
  GPIO.cleanup()

def led_rgbrandom(led,period,colors):
  ''' Light up the selected led, for period in seconds,
  in one of the possible colors. The colors can be
  1 to 3 for RGB, or 1-6 for RGB plus combinations,
  1-7 includes white. Anything over 7 will be set as
  OFF (larger the number more chance of OFF).'''
  value = randint(1,colors)
  if value < len(RGB_LIST):
    led_time(led,RGB_LIST[value-1],period)


def main():
  '''Directly run test function.
  This function will run if the file is executed directly'''
  led_setup()
  led_time(LED1,RGB_RED,5)
  led_time(LED2,RGB_GREEN,5)
  led_time(LED3,RGB_BLUE,5)
  led_time(LED,RGB_MAGENTA,2)
  led_time(LED,RGB_YELLOW,2)
  led_time(LED,RGB_CYAN,2)
  for i in range(20):
    for j in LED:
      #Select from all, plus OFF
      led_rgbrandom(j,0.1,20)


if __name__=='__main__':
  try:
    main()
  finally:
    led_cleanup()
#End
