#!/usr/bin/python3
# scroller.py
import tkinter as TK
import time
import math
from random import randint

STEP=7
xVAL,yVAL=0,1
MAX_WIDTH,MAX_HEIGHT=640,480
SPACE_WIDTH=MAX_WIDTH*2
SPACE_HEIGHT=MAX_HEIGHT*2
LEFT,UP,RIGHT,DOWN=0,1,2,3
SPACE_LIMITS=[0,0,SPACE_WIDTH-MAX_WIDTH,
              SPACE_HEIGHT-MAX_HEIGHT]
DIS_LIMITS=[STEP,STEP,MAX_WIDTH-STEP,MAX_HEIGHT-STEP]
BGN_IMG="bg.gif"
PLAYER_IMG=["playerL.gif","playerU.gif",
            "playerR.gif","playerD.gif"]
WALL_IMG=["wallH.gif","wallV.gif"]
GOLD_IMG="gold.gif"
MARK_IMG="mark.gif"
newGame=False
checks=list()

def move_right(event):
  movePlayer(RIGHT,STEP)
def move_left(event):
  movePlayer(LEFT,-STEP)
def move_up(event):
  movePlayer(UP,-STEP)
def move_down(event):
  movePlayer(DOWN,STEP)

def foundWall(facing,move):
  hitWall=False
  olCoords=[canv.coords(player)[xVAL],
            canv.coords(player)[yVAL],
            canv.coords(player)[xVAL]+PLAYER_SIZE[xVAL],
            canv.coords(player)[yVAL]+PLAYER_SIZE[yVAL]]
  olCoords[facing]+=move
  objects = canv.find_overlapping(olCoords[0],olCoords[1],
                                  olCoords[2],olCoords[3])
  for obj in objects:
    objTags = canv.gettags(obj)
    for tag in objTags:
      if tag == "wall":
        hitWall=True
  return hitWall

def moveBackgnd(movement):
  global bg_offset
  bg_offset[xVAL]+=movement[xVAL]
  bg_offset[yVAL]+=movement[yVAL]
  for obj in canv.find_withtag("bg"):
    canv.move(obj, -movement[xVAL], -movement[yVAL]) 

def makeMove(facing,move):
  if facing == RIGHT or facing == LEFT:
    movement=[move,0] #RIGHT/LEFT
    bgOffset=bg_offset[xVAL]
    playerPos=canv.coords(player)[xVAL]
  else:
    movement=[0,move] #UP/DOWN
    bgOffset=bg_offset[yVAL]
    playerPos=canv.coords(player)[yVAL]
  #Check Bottom/Right Corner
  if facing == RIGHT or facing == DOWN:
    if (playerPos+PLAYER_SIZE[xVAL]) < DIS_LIMITS[facing]:
      canv.move(player, movement[xVAL], movement[yVAL])
    elif bgOffset < SPACE_LIMITS[facing]:
      moveBackgnd(movement)
  else:   #Check Top/Left Corner
    if (playerPos) > DIS_LIMITS[facing]:
      canv.move(player, movement[xVAL], movement[yVAL])
    elif bgOffset > SPACE_LIMITS[facing]:
      moveBackgnd(movement)

def movePlayer(facing,move):
  hitWall=foundWall(facing,move)
  if hitWall==False:
    makeMove(facing,move)
  canv.itemconfig(player,image=playImg[facing])

def check(event):
  global checks,newGame,text
  if newGame:
    for chk in checks:
      canv.delete(chk)
    del checks[:]
    canv.delete(gold,text)
    newGame=False
    hideGold()
  else:
    checks.append(
            canv.create_image(canv.coords(player)[xVAL],
                              canv.coords(player)[yVAL],
                              anchor=TK.NW, image=checkImg,
                              tags=('check','bg')))
    distance=measureTo(checks[-1],gold)
    if(distance<=0):
      canv.itemconfig(gold,state='normal')
      canv.itemconfig(check,state='hidden')
      text = canv.create_text(300,100,fill="white",
                      text=("You have found the gold in"+
                            " %d tries!"%len(checks)))
      newGame=True
    else:
      text = canv.create_text(300,100,fill="white",
                text=("You are %d steps away!"%distance))
      canv.update()
      time.sleep(1)
      canv.delete(text)

def measureTo(objectA,objectB):
  deltaX=canv.coords(objectA)[xVAL]-\
                      canv.coords(objectB)[xVAL]
  deltaY=canv.coords(objectA)[yVAL]-\
                      canv.coords(objectB)[yVAL]
  w_sq=abs(deltaX)**2
  h_sq=abs(deltaY)**2
  hypot=math.sqrt(w_sq+h_sq)
  return round((hypot/5)-20,-1)

def hideGold():
  global gold
  goldPos=findLocationForGold()
  gold=canv.create_image(goldPos[xVAL], goldPos[yVAL],
                         anchor=TK.NW, image=goldImg,
                         tags=('gold','bg'),
                         state='hidden')

def findLocationForGold():
  placeGold=False
  while(placeGold==False):
    goldPos=[randint(0-bg_offset[xVAL],
           SPACE_WIDTH-GOLD_SIZE[xVAL]-bg_offset[xVAL]),
           randint(0-bg_offset[yVAL],
           SPACE_HEIGHT-GOLD_SIZE[yVAL]-bg_offset[yVAL])]
    objects = canv.find_overlapping(goldPos[xVAL],
                          goldPos[yVAL],
                          goldPos[xVAL]+GOLD_SIZE[xVAL],
                          goldPos[yVAL]+GOLD_SIZE[yVAL])
    findNewPlace=False   
    for obj in objects:
      objTags = canv.gettags(obj)
      for tag in objTags:
        if (tag == "wall") or (tag == "player"):
          findNewPlace=True
    if findNewPlace == False:
      placeGold=True
  return goldPos

root = TK.Tk()
root.title("Overhead Game")
root.geometry('%sx%s+%s+%s' %(MAX_WIDTH,
                              MAX_HEIGHT,
                              100, 100))
root.resizable(width=TK.FALSE, height=TK.FALSE)
root.bind('<Right>', move_right)
root.bind('<Left>', move_left)
root.bind('<Up>', move_up)
root.bind('<Down>', move_down)
root.bind('<Return>', check)

canv = TK.Canvas(root, highlightthickness=0)
canv.place(x=0,y=0,width=SPACE_WIDTH,height=SPACE_HEIGHT)

#Create background tiles
bgnImg = TK.PhotoImage(file=BGN_IMG)
BGN_SIZE = bgnImg.width(),bgnImg.height()
background=list()
COLS=int(SPACE_WIDTH/BGN_SIZE[xVAL])+1
ROWS=int(SPACE_HEIGHT/BGN_SIZE[yVAL])+1
for col in range(0,COLS):
  for row in range(0,ROWS):
    background.append(canv.create_image(col*BGN_SIZE[xVAL],
                      row*BGN_SIZE[yVAL], anchor=TK.NW,
                      image=bgnImg,
                      tags=('background','bg')))
bg_offset=[0,0]

#Create player
playImg=list()
for img in PLAYER_IMG:
  playImg.append(TK.PhotoImage(file=img))
#Assume images are all same size/shape
PLAYER_SIZE=playImg[RIGHT].width(),playImg[RIGHT].height()
player = canv.create_image(100,100, anchor=TK.NW,
                           image=playImg[RIGHT],
                           tags=('player'))

#Create walls
wallImg=[TK.PhotoImage(file=WALL_IMG[0]),
         TK.PhotoImage(file=WALL_IMG[1])]
WALL_SIZE=[wallImg[0].width(),wallImg[0].height()]
wallPosH=[(0,WALL_SIZE[xVAL]*1.5),
          (WALL_SIZE[xVAL],WALL_SIZE[xVAL]*1.5),
          (SPACE_WIDTH-WALL_SIZE[xVAL],WALL_SIZE[xVAL]*1.5),
          (WALL_SIZE[xVAL],SPACE_HEIGHT-WALL_SIZE[yVAL])]
wallPosV=[(WALL_SIZE[xVAL],0),(WALL_SIZE[xVAL]*3,0)]
wallPos=[wallPosH,wallPosV]
wall=list()
for i,img in enumerate(WALL_IMG):
  for item in wallPos[i]:
    wall.append(canv.create_image(item[xVAL],item[yVAL],
                                  anchor=TK.NW,
                                  image=wallImg[i],
                                  tags=('wall','bg')))

#Place gold
goldImg = TK.PhotoImage(file=GOLD_IMG)
GOLD_SIZE=[goldImg.width(),goldImg.height()]
hideGold()
#Check mark
checkImg = TK.PhotoImage(file=MARK_IMG)
#Wait for actions from user
root.mainloop()
#End
