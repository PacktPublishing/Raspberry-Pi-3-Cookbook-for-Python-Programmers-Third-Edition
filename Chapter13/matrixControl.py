#!/usr/bin/python3
# matrixControl.py
import wiringpi
import time

MAX7219_NOOP        = 0x00
DIG0=0x01; DIG1=0x02; DIG2=0x03; DIG3=0x04
DIG4=0x05; DIG5=0x06; DIG6=0x07; DIG7=0x08
MAX7219_DIGIT=[DIG0,DIG1,DIG2,DIG3,DIG4,DIG5,DIG6,DIG7]
MAX7219_DECODEMODE  = 0x09
MAX7219_INTENSITY   = 0x0A
MAX7219_SCANLIMIT   = 0x0B
MAX7219_SHUTDOWN    = 0x0C
MAX7219_DISPLAYTEST = 0x0F
SPI_CS=0
SPI_SPEED=100000

class matrix():
  def __init__(self,DEBUG=False):
    self.DEBUG=DEBUG
    wiringpi.wiringPiSPISetup(SPI_CS,SPI_SPEED)
    self.sendCmd(MAX7219_SCANLIMIT, 7)   # enable outputs
    self.sendCmd(MAX7219_DECODEMODE, 0)  # no digit decode
    self.sendCmd(MAX7219_DISPLAYTEST, 0) # display test off
    self.clear()
    self.brightness(15)                   # brightness 0-15
    self.sendCmd(MAX7219_SHUTDOWN, 1)    # start display
  def sendCmd(self, register, data):
    buffer=(register<<8)+data
    buffer=buffer.to_bytes(2, byteorder='big')
    if self.DEBUG:print("Send byte: 0x%04x"%
                        int.from_bytes(buffer,'big'))
    wiringpi.wiringPiSPIDataRW(SPI_CS,buffer)
    if self.DEBUG:print("Response:  0x%04x"%
                        int.from_bytes(buffer,'big'))
    return buffer
  def clear(self):
    if self.DEBUG:print("Clear")
    for row in MAX7219_DIGIT:
      self.sendCmd(row + 1, 0)
  def brightness(self,intensity):
    self.sendCmd(MAX7219_INTENSITY, intensity % 16)

def letterK(matrix):
    print("K")
    K=(0x0066763e1e366646).to_bytes(8, byteorder='big')
    for idx,value in enumerate(K):
        matrix.sendCmd(idx+1,value)

def main():
    myMatrix=matrix(DEBUG=True)
    letterK(myMatrix)
    while(1):
      time.sleep(5)
      myMatrix.clear()
      time.sleep(5)
      letterK(myMatrix)

def main2():	  
    myMatrix=matrix(DEBUG=True)
    print("Display TEST OFF")
    myMatrix.sendCmd(MAX7219_DISPLAYTEST, 0) # display test OFF
    time.sleep(2)
    print("Display TEST ON")
    myMatrix.sendCmd(MAX7219_DISPLAYTEST, 1) # display test ON
    time.sleep(2)
    print("Display TEST OFF")
    myMatrix.sendCmd(MAX7219_DISPLAYTEST, 0) # display test OFF
    time.sleep(2)
    print("Display")
    myMatrix.sendCmd(1, 0x55)
    time.sleep(2)
    print("Display Show")
    while(1):
        for a in range(255):
            for b in range(8):
                time.sleep(0.1)
                print(b+1,":",a)
                myMatrix.sendCmd(b+1,a)


	
if __name__ == '__main__':
    main()
#End
