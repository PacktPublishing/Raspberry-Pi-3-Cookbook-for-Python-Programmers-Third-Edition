#!/usr/bin/python3
#painting.py
import tkinter as TK

#Set defaults
btn1pressed = False
newline = True

def main():
  root = TK.Tk()
  the_canvas = TK.Canvas(root)
  the_canvas.pack()
  the_canvas.bind("<Motion>", mousemove)
  the_canvas.bind("<ButtonPress-1>", mouse1press)
  the_canvas.bind("<ButtonRelease-1>", mouse1release)
  root.mainloop()

def mouse1press(event):
  global btn1pressed
  btn1pressed = True

def mouse1release(event):
  global btn1pressed, newline
  btn1pressed = False
  newline = True

def mousemove(event):
  if btn1pressed == True:
    global xorig, yorig, newline
    if newline == False:
      event.widget.create_line(xorig,yorig,event.x,event.y,
                                             smooth=TK.TRUE)
    newline = False
    xorig = event.x
    yorig = event.y

if __name__ == "__main__":
  main()
#End
