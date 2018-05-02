#!/usr/bin/python3
#gpiokeys-mouse.py
import time
import RPi.GPIO as GPIO
import uinput

#HARDWARE SETUP
# P1
# 2[==G=====<=V==]26
# 1[===2=1>^=====]25
B_DOWN  = 22    #V
B_LEFT  = 18   #<
B_UP    = 15   #^
B_RIGHT = 13   #>
B_1  = 11   #1
B_2  = 7   #2

DEBUG=False

BTN = [B_UP,B_DOWN,B_LEFT,B_RIGHT,B_1,B_2]
#MSG = ["UP","DOWN","LEFT","RIGHT","1","2"]
MSG = ["M_UP","M_DOWN","M_LEFT","M_RIGHT","1","Enter"]

#Setup the DPad module pins and pull-ups
def dpad_setup():
  #Set up the wiring
  GPIO.setmode(GPIO.BOARD)
  # Setup BTN Ports as INPUTS
  for val in BTN:
    # set up GPIO input with pull-up control
    #(pull_up_down can be:
    #    PUD_OFF, PUD_UP or PUD_DOWN, default PUD_OFF)
    GPIO.setup(val, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
  #Setup uinput
  events_mouse=(uinput.REL_Y,uinput.REL_Y, uinput.REL_X,
                uinput.REL_X,uinput.BTN_LEFT,uinput.BTN_RIGHT)
  events = events_mouse
  device = uinput.Device(events)
  time.sleep(2) # seconds
  dpad_setup()
  print("DPad Ready!")

  btn_state=[False,False,False,False,False,False]
  key_state=[False,False,False,False,False,False]
  while True:
    #Catch all the buttons pressed before pressing the related keys
    for idx, val in enumerate(BTN):
      if GPIO.input(val) == False:
        btn_state[idx]=True
      else:
        btn_state[idx]=False

    #Perform the button presses/releases
    #(but only change state once)
    for idx, val in enumerate(btn_state):
      if MSG[idx] == "M_UP" or MSG[idx] == "M_LEFT":
        state = -1
      else:
        state = 1
      if val == True:
        device.emit(events[idx], state) # Press.
      elif val == False:
        device.emit(events[idx], 0) # Release.

    time.sleep(0.01)
    
try:
  main()
finally:
  GPIO.cleanup()
#End
