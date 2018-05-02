#!/usr/bin/env python3
#avoidance.py
import rover_drive as drive
import wiringpi2
import time

opCmds={'f':'bl','b':'fr','r':'ll','l':'rr','#':'#'}
PINS=[7,11,12,13]   # PINS=[L_FWD,L_BWD,R_FWD,R_BWD]
ON=1;OFF=0
IN=0;OUT=1
PULL_UP=2;PULL_DOWN=1

class sensor:
  # Constructor
  def __init__(self,pins=PINS):
    self.pins = pins
    self.GPIOsetup()

  def GPIOsetup(self):
    wiringpi2.wiringPiSetupPhys()
    for gpio in self.pins:
      wiringpi2.pinMode(gpio,IN)
      wiringpi2.pullUpDnControl(gpio,PULL_UP)    

  def checkSensor(self):
    hit = False
    for gpio in self.pins:
      if wiringpi2.digitalRead(gpio)==False:
        hit = True
    return hit

def main():
  myBot=drive.motor()
  mySensors=sensor()
  while(True):
    print("Enter CMDs [f,b,r,l,#]:")
    CMD=input()
    for idx,char in enumerate(CMD.lower()):
      print("Step %s of %s: %s"%(idx+1,len(CMD),char))
      myBot.cmd(char,step=0.01)#small steps
      hit = mySensors.checkSensor()
      if hit:
        print("We hit something on move: %s Go: %s"%(char,
                                              opCmds[char]))
        for charcmd in opCmds[char]:
          myBot.cmd(charcmd,step=0.01)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End
