#!/usr/bin/python3
#missileMenu.py
import tkinter as TK
import missileControl as MC

BTN_SIZE=10

def menuInit():
  btnLeft = TK.Button(root, text="Left",
                      command=sendLeft, width=BTN_SIZE)   
  btnRight = TK.Button(root, text="Right",
                       command=sendRight, width=BTN_SIZE)   
  btnUp = TK.Button(root, text="Up",
                    command=sendUp, width=BTN_SIZE)   
  btnDown = TK.Button(root, text="Down",
                      command=sendDown, width=BTN_SIZE)
  btnFire = TK.Button(root, text="Fire",command=sendFire,
                      width=BTN_SIZE, bg="red")
  btnLeft.grid(row=2,column=0)
  btnRight.grid(row=2,column=2)
  btnUp.grid(row=1,column=1)
  btnDown.grid(row=3,column=1)
  btnFire.grid(row=2,column=1)

def sendLeft():
  print("Left")
  myMissile.left()
       
def sendRight():
  print("Right")    
  myMissile.right()
       
def sendUp():
  print("Up")
  myMissile.up()
       
def sendDown():
  print("Down")
  myMissile.down()
       
def sendFire():
  print("Fire")
  myMissile.fire()
       

root = TK.Tk()
root.title("Missile Command")
prompt = "Select action"
label1 = TK.Label(root, text=prompt, width=len(prompt),
                  justify=TK.CENTER, bg='lightblue')
label1.grid(row=0,column=0,columnspan=3)
menuInit()
with MC.Missile() as myMissile:
  root.mainloop()
#End
