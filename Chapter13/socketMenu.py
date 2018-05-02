#!/usr/bin/python3
#socketMenu.py
import tkinter as TK
import socketControl as SC

#Define Switches ["Switch name","Switch number"]
switch1 = ["Living Room Lamp",1]
switch2 = ["Coffee Machine",2]
switch3 = ["Bedroom Fan",3]
sw_list = [switch1,switch2,switch3]
SW_NAME = 0; SW_CMD  = 1
SW_COLOR=["gray","green"]

class swButtons:
  def __init__(self,gui,sw_index,switchCtrl):
    #Add the buttons to window
    self.msgType=TK.IntVar()
    self.msgType.set(SC.MSGOFF)
    self.btn = TK.Button(gui,
                  text=sw_list[sw_index][SW_NAME],
                  width=30, command=self.sendMsg,
                  bg=SW_COLOR[self.msgType.get()])
    self.btn.pack()
    msgOn = TK.Radiobutton(gui,text="On",
              variable=self.msgType, value=SC.MSGON)
    msgOn.pack()
    msgOff = TK.Radiobutton(gui,text="Off",
              variable=self.msgType,value=SC.MSGOFF)
    msgOff.pack()
    self.sw_num=sw_list[sw_index][SW_CMD]
    self.sw_ctrl=switchCtrl
  def sendMsg(self):
    print ("SW_CMD: %s %d" % (self.sw_num,
                              self.msgType.get()))
    self.btn.configure(bg=SW_COLOR[self.msgType.get()])
    self.sw_ctrl.message(self.sw_num,
                         self.msgType.get())

root = TK.Tk()
root.title("Remote Switches")
prompt = "Control a switch"
label1 = TK.Label(root, text=prompt, width=len(prompt),
                  justify=TK.CENTER, bg='lightblue')
label1.pack()
#Create the switch
with SC.Switch() as mySwitches:
  #Create menu buttons from sw_list
  for index, app in enumerate(sw_list):
    swButtons(root,index,mySwitches)
  root.mainloop()
#End
