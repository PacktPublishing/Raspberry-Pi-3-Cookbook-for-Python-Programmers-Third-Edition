#!/usr/bin/python3
#matrixMenu.py
import tkinter as TK
import time
import matrixControl as MC

#Enable/Disable DEBUG
DEBUG = True
#Set display sizes
BUTTON_SIZE = 10
NUM_BUTTON = 8
NUM_LIGHTS=NUM_BUTTON*NUM_BUTTON
MAX_VALUE=0xFFFFFFFFFFFFFFFF
MARGIN = 2
WINDOW_H = MARGIN+((BUTTON_SIZE+MARGIN)*NUM_BUTTON)
WINDOW_W = WINDOW_H
TEXT_WIDTH=int(2+((NUM_BUTTON*NUM_BUTTON)/4))
LIGHTOFFON=["red4","red"]
OFF = 0; ON = 1
colBg = "black"

def isBitSet(value,bit):
  return (value>>bit & 1)

def setBit(value,bit,state=1):
  mask=1<<bit
  if state==1:
    value|=mask
  else:
    value&=~mask
  return value

def toggleBit(value,bit):
  state=isBitSet(value,bit)
  value=setBit(value,bit,not state)
  return value

class matrixGUI(TK.Frame):
  def __init__(self,parent,matrix):
    self.parent = parent
    self.matrix=matrix
    #Light Status
    self.lightStatus=0
    #Add a canvas area ready for drawing on
    self.canvas = TK.Canvas(parent, width=WINDOW_W,
                        height=WINDOW_H, background=colBg)
    self.canvas.pack()
    #Add some "lights" to the canvas
    self.light = []
    for iy in range(NUM_BUTTON):
      for ix in range(NUM_BUTTON):
        x = MARGIN+MARGIN+((MARGIN+BUTTON_SIZE)*ix)
        y = MARGIN+MARGIN+((MARGIN+BUTTON_SIZE)*iy)
        self.light.append(self.canvas.create_rectangle(x,y,
                              x+BUTTON_SIZE,y+BUTTON_SIZE,
                              fill=LIGHTOFFON[OFF]))
    #Add other items
    self.codeText=TK.StringVar()
    self.codeText.trace("w", self.changedCode)
    self.generateCode()
    code=TK.Entry(parent,textvariable=self.codeText,
                  justify=TK.CENTER,width=TEXT_WIDTH)
    code.pack()
    #Bind to canvas not tk (only respond to lights)
    self.canvas.bind('<Button-1>', self.mouseClick)
  
  def mouseClick(self,event):
    itemsClicked=self.canvas.find_overlapping(event.x,
                             event.y,event.x+1,event.y+1)
    for item in itemsClicked:
      self.toggleLight(item)

  def setLight(self,num):
    state=isBitSet(self.lightStatus,num)
    self.canvas.itemconfig(self.light[num],
                           fill=LIGHTOFFON[state])
    
  def toggleLight(self,num):
    if num != 0:
      self.lightStatus=toggleBit(self.lightStatus,num-1)
      self.setLight(num-1)
      self.generateCode()

  def generateCode(self):
    self.codeText.set("0x%016x"%self.lightStatus)

  def changedCode(self,*args):
    updated=False
    try:
      codeValue=int(self.codeText.get(),16)
      if(codeValue>MAX_VALUE):
        codeValue=codeValue>>4
      self.updateLight(codeValue)
      updated=True
    except:
      self.generateCode()
      updated=False
    return updated

  def updateLight(self,lightsetting):
    self.lightStatus=lightsetting
    for num in range(NUM_LIGHTS):
      self.setLight(num)
    self.generateCode()
    self.updateHardware()

  def updateHardware(self):
    sendBytes=self.lightStatus.to_bytes(NUM_BUTTON,
                                        byteorder='big')
    print(sendBytes)
    for idx,row in enumerate(MC.MAX7219_DIGIT):
      response = self.matrix.sendCmd(row,sendBytes[idx])
      print(response)

def main():
  global root
  root=TK.Tk()
  root.title("Matrix GUI")
  myMatrixHW=MC.matrix(DEBUG)
  myMatrixGUI=matrixGUI(root,myMatrixHW)
  TK.mainloop()
    
if __name__ == '__main__':
    main()
#End
