#!/usr/bin/python3
# bouncingball.py
import tkinter as TK
import time

VERT,HOREZ=0,1
xTOP,yTOP = 0,1
xBTM,yBTM = 2,3
MAX_WIDTH,MAX_HEIGHT = 640,480
xSTART,ySTART = 100,200
BALL_SIZE=20
RUNNING=True

def close():
  global RUNNING
  RUNNING=False
  root.destroy()
    
def move_right(event):
  if canv.coords(paddle)[xBTM]<(MAX_WIDTH-7):
    canv.move(paddle, 7, 0)

def move_left(event):
  if canv.coords(paddle)[xTOP]>7:
    canv.move(paddle, -7, 0)

def determineDir(ball,obj):
  global delta_x,delta_y
  if (ball[xTOP] == obj[xBTM]) or (ball[xBTM] == obj[xTOP]):
    delta_x = -delta_x            
  elif (ball[yTOP] == obj[yBTM]) or (ball[yBTM] == obj[yTOP]):
    delta_y = -delta_y

root = TK.Tk()
root.title("Bouncing Ball")
root.geometry('%sx%s+%s+%s' %(MAX_WIDTH, MAX_HEIGHT, 100, 100))
root.bind('<Right>', move_right)
root.bind('<Left>', move_left)
root.protocol('WM_DELETE_WINDOW', close)

canv = TK.Canvas(root, highlightthickness=0)
canv.pack(fill='both', expand=True)

top = canv.create_line(0, 0, MAX_WIDTH, 0, fill='blue',
                       tags=('top'))
left = canv.create_line(0, 0, 0, MAX_HEIGHT, fill='blue',
                        tags=('left'))
right = canv.create_line(MAX_WIDTH, 0, MAX_WIDTH, MAX_HEIGHT,
                    fill='blue', tags=('right'))
bottom = canv.create_line(0, MAX_HEIGHT, MAX_WIDTH, MAX_HEIGHT,
                    fill='blue', tags=('bottom'))

ball = canv.create_rectangle(0, 0, BALL_SIZE, BALL_SIZE,
                    outline='black', fill='black', tags=('ball'))
paddle = canv.create_rectangle(100, MAX_HEIGHT - 30, 150, 470,
                    outline='black', fill='green', tags=('rect'))

brick=list()
for i in range(0,16):
  for row in range(0,4):
    brick.append(canv.create_rectangle(i*40, row*20,
                       ((i+1)*40)-2, ((row+1)*20)-2,
                        outline='black', fill='red',
                        tags=('rect')))

delta_x = delta_y = 1
xold,yold = xSTART,ySTART
canv.move(ball, xold, yold)

while RUNNING:
  objects = canv.find_overlapping(canv.coords(ball)[0],
                                  canv.coords(ball)[1],
                                  canv.coords(ball)[2],
                                  canv.coords(ball)[3])
  #Only change the direction once (so will bounce off 1st
  # block even if 2 are hit)
  dir_changed=False
  for obj in objects:
    if (obj != ball):
      if dir_changed==False:
        determineDir(canv.coords(ball),canv.coords(obj))
        dir_changed=True
      if (obj >= brick[0]) and (obj <= brick[len(brick)-1]):
        canv.delete(obj)
      if (obj == bottom):
        text = canv.create_text(300,100,text="YOU HAVE MISSED!")
        canv.coords(ball, (xSTART,ySTART,
                           xSTART+BALL_SIZE,ySTART+BALL_SIZE))
        delta_x = delta_y = 1
        canv.update()
        time.sleep(3)
        canv.delete(text)
  new_x, new_y = delta_x, delta_y
  canv.move(ball, new_x, new_y)

  canv.update()
  time.sleep(0.005)
#End
