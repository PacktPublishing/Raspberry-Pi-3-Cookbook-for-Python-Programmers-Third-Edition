#!/usr/bin/python3
#serialControl.py
import serial
import time

#Serial Port settings
SERNAME="/dev/ttyUSB0"
#SERNAME="/dev/ttyAMA0"
#default setting is 9600,8,N,1
IDLE=0; SEND=1; RECEIVE=1

def b2s(message):
  '''Byte to String'''
  return bytes.decode(message)
def s2b(message):
  '''String to Byte'''
  return bytearray(message,"ascii")

class serPort():
  def __init__(self,serName="/dev/ttyAMA0"):
    self.ser = serial.Serial(serName)
    print (self.ser.name)
    print (self.ser)
    self.state=IDLE
  def __enter__(self):
    return self
  def send(self,message):
    if self.state==IDLE and self.ser.isOpen():
      self.state=SEND
      self.ser.write(s2b(message))
      self.state=IDLE

  def receive(self, chars=1, timeout=5, echo=True,
              terminate="\r"):
    message=""
    if self.state==IDLE and self.ser.isOpen():
      self.state=RECEIVE
      self.ser.timeout=timeout
      while self.state==RECEIVE:
        echovalue=""
        while self.ser.inWaiting() > 0:
          echovalue += b2s(self.ser.read(chars))
        if echo==True:
          self.ser.write(s2b(echovalue))
        message+=echovalue
        if terminate in message:
          self.state=IDLE
    return message
  def __exit__(self,type,value,traceback):
    self.ser.close()      

def main():
  try:
    with serPort(serName=SERNAME) as mySerialPort:
      mySerialPort.send("Send some data to me!\r\n")
      while True:
        print ("Waiting for input:")
        print (mySerialPort.receive())
  except OSError:
    print ("Check selected port is valid: %s" %serName)
  except KeyboardInterrupt:
    print ("Finished")

if __name__=="__main__":
  main()
#End
