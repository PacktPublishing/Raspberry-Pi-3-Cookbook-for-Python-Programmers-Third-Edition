#!/usr/bin/env python3
#servoAdafruit.py
import wiringpi2
import time

#PWM Registers
MODE1=0x00
PRESCALE=0xFE
LED0_ON_L=0x06
LED0_ON_H=0x07
LED0_OFF_L=0x08
LED0_OFF_H=0x09

PWMHZ=50
PWMADR=0x40


class servo:
  # Constructor
  def __init__(self,pwmFreq=PWMHZ,addr=PWMADR):
    self.i2c = wiringpi2.I2C()
    self.devPWM=self.i2c.setup(addr)
    self.GPIOsetup(pwmFreq,addr)

  def GPIOsetup(self,pwmFreq,addr):
    self.i2c.read(self.devPWM)
    self.pwmInit(pwmFreq)

  def pwmInit(self,pwmFreq):
    prescale = 25000000.0 / 4096.0   # 25MHz / 12-bit
    prescale /= float(pwmFreq)
    prescale = prescale - 0.5 #-1 then +0.5 to round to
                              # nearest value
    prescale = int(prescale)
    self.i2c.writeReg8(self.devPWM,MODE1,0x00) #RESET
    mode=self.i2c.read(self.devPWM)
    self.i2c.writeReg8(self.devPWM,MODE1,
                       (mode & 0x7F)|0x10) #SLEEP
    self.i2c.writeReg8(self.devPWM,PRESCALE,prescale)
    self.i2c.writeReg8(self.devPWM,MODE1,mode) #restore mode
    time.sleep(0.005)
    self.i2c.writeReg8(self.devPWM,MODE1,mode|0x80) #restart

  def setPWM(self,channel, on, off):
    on=int(on)
    off=int(off)
    self.i2c.writeReg8(self.devPWM,
                       LED0_ON_L+4*channel,on & 0xFF)
    self.i2c.writeReg8(self.devPWM,LED0_ON_H+4*channel,on>>8)
    self.i2c.writeReg8(self.devPWM,
                       LED0_OFF_L+4*channel,off & 0xFF)
    self.i2c.writeReg8(self.devPWM,LED0_OFF_H+4*channel,off>>8)

def main():
  servoMin = 205  # Min pulse 1ms 204.8 (50Hz)
  servoMax = 410  # Max pulse 2ms 409.6 (50Hz)
  myServo=servo()
  myServo.setPWM(0,0,servoMin)
  time.sleep(2)
  myServo.setPWM(0,0,servoMax)
  
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
#End

