#!/usr/bin/python3
# missileControl.py
import time
import usb.core

class SamMissile():
  idVendor=0x1130
  idProduct=0x0202
  idName="Tenx Technology SAM Missile"
  # Protocol control bytes
  bmRequestType=0x21
  bmRequest=0x09
  wValue=0x02
  wIndex=0x01
  # Protocol command bytes
  INITA     = [ord('U'), ord('S'), ord('B'), ord('C'),
               0,  0,  4,  0]
  INITB     = [ord('U'), ord('S'), ord('B'), ord('C'),
               0, 64,  2,  0]
  CMDFILL   = [ 8,  8,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0]#48 zeros
  STOP      = [ 0,  0,  0,  0,  0,  0]
  LEFT      = [ 0,  1,  0,  0,  0,  0]
  RIGHT     = [ 0,  0,  1,  0,  0,  0]
  UP        = [ 0,  0,  0,  1,  0,  0]
  DOWN      = [ 0,  0,  0,  0,  1,  0]
  LEFTUP    = [ 0,  1,  0,  1,  0,  0]
  RIGHTUP   = [ 0,  0,  1,  1,  0,  0]
  LEFTDOWN  = [ 0,  1,  0,  0,  1,  0]
  RIGHTDOWN = [ 0,  0,  1,  0,  1,  0]
  FIRE      = [ 0,  0,  0,  0,  0,  1]
  def __init__(self):
    self.dev = usb.core.find(idVendor=self.idVendor,
                                idProduct=self.idProduct)
  def move(self,cmd,duration):
    print("Move:%s %d sec"% (cmd,duration))
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest,self.wValue,
                           self.wIndex, self.INITA)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest,self.wValue,
                           self.wIndex, self.INITB)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest, self.wValue,
                           self.wIndex, cmd+self.CMDFILL)
    time.sleep(duration)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest, self.wValue,
                           self.wIndex, self.INITA)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest, self.wValue,
                           self.wIndex, self.INITB)
    self.dev.ctrl_transfer(self.bmRequestType,
                      self.bmRequest, self.wValue,
                      self.wIndex, self.STOP+self.CMDFILL)
 
class ChesenMissile():
  idVendor=0x0a81
  idProduct=0x0701
  idName="Chesen Electronics/Dream Link"
  # Protocol control bytes
  bmRequestType=0x21
  bmRequest=0x09
  wValue=0x0200
  wIndex=0x00
  # Protocol command bytes
  DOWN    = [0x01]
  UP      = [0x02]
  LEFT    = [0x04]
  RIGHT   = [0x08]
  FIRE    = [0x10]
  STOP    = [0x20]
  def __init__(self):
    self.dev = usb.core.find(idVendor=self.idVendor,
                             idProduct=self.idProduct)
  def move(self,cmd,duration):
    print("Move:%s"%cmd)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest,
                           self.wValue, self.wIndex, cmd)
    time.sleep(duration)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest, self.wValue,
                           self.wIndex, self.STOP)

class ThunderMissile():
  idVendor=0x2123
  idProduct=0x1010
  idName="Dream Cheeky Thunder"
  # Protocol control bytes
  bmRequestType=0x21
  bmRequest=0x09
  wValue=0x00
  wIndex=0x00
  # Protocol command bytes
  CMDFILL = [0,0,0,0,0,0]
  DOWN    = [0x02,0x01]
  UP      = [0x02,0x02]
  LEFT    = [0x02,0x04]
  RIGHT   = [0x02,0x08]
  FIRE    = [0x02,0x10]
  STOP    = [0x02,0x20]
  def __init__(self):
    self.dev = usb.core.find(idVendor=self.idVendor,
                             idProduct=self.idProduct)
  def move(self,cmd,duration):
    print("Move:%s"%cmd)
    self.dev.ctrl_transfer(self.bmRequestType,
                           self.bmRequest, self.wValue,
                           self.wIndex, cmd+self.CMDFILL)
    time.sleep(duration)
    self.dev.ctrl_transfer(self.bmRequestType,
                      self.bmRequest, self.wValue,
                      self.wIndex, self.STOP+self.CMDFILL)


class Missile():
  def __init__(self):
    print("Initialize Missiles")
    self.usbDevice=SamMissile()
    
    if self.usbDevice.dev is not None:
      print("Device Initialized:" +
            " %s" % self.usbDevice.idName)
      #Detach the kernel driver if active
      if self.usbDevice.dev.is_kernel_driver_active(0):
        print("Detaching kernel driver 0")
        self.usbDevice.dev.detach_kernel_driver(0)
      if self.usbDevice.dev.is_kernel_driver_active(1):
        print("Detaching kernel driver 1")
        self.usbDevice.dev.detach_kernel_driver(1)
      self.usbDevice.dev.set_configuration()
    else:
      raise Exception("Missile device not found")
  def __enter__(self):
    return self
  def left(self,duration=1):
    self.usbDevice.move(self.usbDevice.LEFT,duration)
  def right(self,duration=1):
    self.usbDevice.move(self.usbDevice.RIGHT,duration)
  def up(self,duration=1):
    self.usbDevice.move(self.usbDevice.UP,duration)
  def down(self,duration=1):
    self.usbDevice.move(self.usbDevice.DOWN,duration)
  def fire(self,duration=1):
    self.usbDevice.move(self.usbDevice.FIRE,duration)
  def stop(self,duration=1):
    self.usbDevice.move(self.usbDevice.STOP,duration)
  def __exit__(self, type, value, traceback):
    print("Exit")

def main():
  try:
    with Missile() as myMissile:
      myMissile.down()
      time.sleep(2)
      myMissile.up()
  except Exception as detail:
    print("Error: %s" % detail)
    
if __name__ == '__main__':
    main()
#End
