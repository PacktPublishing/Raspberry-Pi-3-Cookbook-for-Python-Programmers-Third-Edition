#!/usr/bin/python3
#rgbledrainbow.py
import time
import rgbled as RGBLED

def next_value(number,max):
  number = number % max
  return number

def main():
  print ("Setup the RGB module")
  RGBLED.led_setup()

  # Multiple LEDs with different Colors
  print ("Switch on Rainbow")
  led_num = 0
  col_num = 0
  for l in range(5):
    print ("Cycle LEDs")
    for k in range(100):
      #Set the starting point for the next set of colors
      col_num = next_value(col_num+1,len(RGBLED.RGB_COLORS))
      for i in range(20):  #cycle time
        for j in range(5): #led cycle
          led_num = next_value(j,len(RGBLED.LED))
          led_color = next_value(col_num+led_num,
                                 len(RGBLED.RGB_COLORS))
          RGBLED.led_combo(RGBLED.LED[led_num],
                           RGBLED.RGB_COLORS[led_color],0.001)

    print ("Cycle COLORs")        
    for k in range(100):
      #Set the next color
      col_num = next_value(col_num+1,len(RGBLED.RGB_COLORS))
      for i in range(20): #cycle time
        for j in range(5): #led cycle
          led_num = next_value(j,len(RGBLED.LED))
          RGBLED.led_combo(RGBLED.LED[led_num],
                           RGBLED.RGB_COLORS[col_num],0.001)
  print ("Finished")

if __name__=='__main__':
  try:
    main()
  finally:
    RGBLED.led_cleanup()
#End
