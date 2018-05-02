#!/usr/bin/python3
import wiringpi2
import time
import datetime
import data_adc as dataDevice

AF_BASE=100
AF_E=AF_BASE+13; AF_RW=AF_BASE+14; AF_RS=AF_BASE+15

AF_DB4=AF_BASE+12; AF_DB5=AF_BASE+11; AF_DB6=AF_BASE+10; AF_DB7=AF_BASE+9

AF_SELECT=AF_BASE+0; AF_RIGHT=AF_BASE+1; AF_DOWN=AF_BASE+2
AF_UP=AF_BASE+3; AF_LEFT=AF_BASE+4; AF_BACK=AF_BASE+5

AF_GREEN=AF_BASE+6; AF_BLUE=AF_BASE+7; AF_RED=AF_BASE+8
BNK=" "*16 #16spaces

def gpiosetup():
  global lcd
  wiringpi2.wiringPiSetup()
  wiringpi2.mcp23017Setup(AF_BASE,0x20)
  wiringpi2.pinMode(AF_RIGHT,0)
  wiringpi2.pinMode(AF_LEFT,0)
  wiringpi2.pinMode(AF_SELECT,0)
  wiringpi2.pinMode(AF_RW,1)
  wiringpi2.digitalWrite(AF_RW,0)
  #lcdInit(int rows, int cols, int bits, int rs, int strb, int d0, int d1, int d2, int d3, int d4, int d5, int d6, int d7)
  lcd=wiringpi2.lcdInit(2,16,4,AF_RS,AF_E,AF_DB4,AF_DB5,AF_DB6,AF_DB7,0,0,0,0)
  #wiringpi2.lcdHome(lcd)
  #wiringpi2.lcdClear(lcd)
  #wiringpi2.lcdPosition(lcd,0,0)

def printLCD(line0="",line1=""):
  wiringpi2.lcdPosition(lcd,0,0)
  wiringpi2.lcdPrintf(lcd,line0+BNK)
  wiringpi2.lcdPosition(lcd,0,1)
  wiringpi2.lcdPrintf(lcd,line1+BNK)

def checkBtn(idx,size):
  global run
  if wiringpi2.digitalRead(AF_LEFT):
    idx-=1
    printLCD()
  elif wiringpi2.digitalRead(AF_RIGHT):
    idx+=1
    printLCD()
  if wiringpi2.digitalRead(AF_SELECT):
    printLCD("Exit Display")
    run=False
  return idx%size
  
def main():
  global run
  gpiosetup()
  myData = dataDevice.device()
  myDataNames=myData.getName()
  run=True
  index=0
  while(run):
    data=myData.getNew()
    printLCD(myDataNames[index],str(data[index]))
    time.sleep(1)
    index = checkBtn(index,len(myDataNames))
    
    

main()

