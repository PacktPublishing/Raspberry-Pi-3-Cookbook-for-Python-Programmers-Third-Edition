#!/usr/bin/python3
#sonic.py
import wiringpi2
import time
import datetime

ON=1;OFF=0; IN=0;OUT=1
TRIGGER=15
ECHO=7
PULSE=0.00001 #10us pulse
SPEEDOFSOUND=34029 #34029 cm/s

def gpiosetup():
  wiringpi2.wiringPiSetupPhys()
  wiringpi2.pinMode(TRIGGER,OUT)
  wiringpi2.pinMode(ECHO,IN)
  wiringpi2.digitalWrite(TRIGGER,OFF)
  time.sleep(0.5)

def pulse():
  wiringpi2.digitalWrite(TRIGGER,ON)
  time.sleep(PULSE)
  wiringpi2.digitalWrite(TRIGGER,OFF)
  starttime=time.time()
  stop=starttime
  start=starttime
  while wiringpi2.digitalRead(ECHO)==0 and start<starttime+2:
    start=time.time()
  while wiringpi2.digitalRead(ECHO)==1 and stop<starttime+2:
    stop=time.time()
  delta=stop-start
  print("Start:%f Stop:%f Delta:%f"%(start,stop,delta))
  distance=delta*SPEEDOFSOUND
  return distance/2.0
  
def main():
  global run
  gpiosetup()
  while(True):
    print("Sample")
    print("Distance:%.1f"%pulse())
    time.sleep(2)
    
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End

