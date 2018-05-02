#!/usr/bin/env python3
#data_adc.py
import wiringpi2
import time

DEBUG=False
LIGHT=0;TEMP=1;EXT=2;POT=3
ADC_CH=[LIGHT,TEMP,EXT,POT]
ADC_ADR=0x48
ADC_CYCLE=0x04
BUS_GAP=0.25
DATANAME=["0:Light","1:Temperature",
          "2:External","3:Potentiometer"]

class device:
  # Constructor:
  def __init__(self,addr=ADC_ADR):
    self.NAME=DATANAME
    self.i2c = wiringpi2.I2C()
    self.devADC=self.i2c.setup(addr)
    pwrup = self.i2c.read(self.devADC) #flush power up value
    if DEBUG==True and pwrup!=-1:
      print("ADC Ready")
    self.i2c.read(self.devADC) #flush first value
    time.sleep(BUS_GAP)
    self.i2c.write(self.devADC,ADC_CYCLE)
    time.sleep(BUS_GAP)
    self.i2c.read(self.devADC) #flush first value

  def getName(self):
    return self.NAME

  def getNew(self):
    data=[]
    for ch in ADC_CH:
      time.sleep(BUS_GAP)
      data.append(self.i2c.read(self.devADC))
    return data

def main():
  ADC = device()
  print (str(ADC.getName()))
  for i in range(10):
    dataValues = ADC.getNew()
    print (str(dataValues))
    time.sleep(1)

if __name__=='__main__':
  main()
#End
