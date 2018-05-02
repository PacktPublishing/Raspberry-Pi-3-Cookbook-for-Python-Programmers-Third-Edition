#!/usr/bin/python3
""" Create a 3D space with a Tetrahedron inside and rotate the
    view around using the mouse.
"""
from math import sin, cos, radians

import demo
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50)
#capture mouse and key presses
inputs=pi3d.InputEvents()

def main():
  CAMERA = pi3d.Camera.instance()
  tex = pi3d.Texture("textures/stripwood.jpg")
  flatsh = pi3d.Shader("uv_flat")

  #Define the coordinates for our shape (x,y,z) 
  A=(-1.0,-1.0,-1.0)
  B=(1.0,-1.0,1.0)
  C=(-1.0,-1.0,1.0)
  D=(-1.0,1.0,1.0)
  ids=["A","B","C","D"]
  coords=[A,B,C,D]
  myTetra = pi3d.Tetrahedron(x=0.0, y=0.0, z=0.0,
                             corners=(A,B,C,D))
  myTetra.set_draw_details(flatsh,[tex])
  # Load ttf font and set the font to black
  arialFont = pi3d.Font("fonts/FreeMonoBoldOblique.ttf",
                        "#000000")
  mystring=[]
  #Create string objects to show the coordinates
  for i,pos in enumerate(coords):
    mystring.append(pi3d.String(font=arialFont,
                            string=ids[i]+str(pos),
                            x=pos[0], y=pos[1],z=pos[2]))
    mystring.append(pi3d.String(font=arialFont,
                            string=ids[i]+str(pos),
                            x=pos[0], y=pos[1],z=pos[2], ry=180))
  for string in mystring:
    string.set_shader(flatsh)

  camRad = 4.0 # radius of camera position
  rot = 0.0 # rotation of camera
  tilt = 0.0 # tilt of camera

  # main display loop
  while DISPLAY.loop_running() and not \
                               inputs.key_state("KEY_ESC"):
    inputs.do_input_events()
    #Note:Some mice devices will be located on
    #get_mouse_movement(1) instead of get_mouse_movement()
    mx,my,mv,mh,md=inputs.get_mouse_movement(1)
    #mx,my,mv,mh,md=inputs.get_mouse_movement(1)
    rot -= (mx)*0.2
    tilt -= (my)*0.2
    CAMERA.reset()
    CAMERA.rotate(-tilt, rot, 0)
    CAMERA.position((camRad * sin(radians(rot)) *
                     cos(radians(tilt)), 
                     camRad * sin(radians(tilt)), 
                     -camRad * cos(radians(rot)) *
                     cos(radians(tilt))))
    #Draw the Tetrahedron
    myTetra.draw()
    for string in mystring:
      string.draw()

try:
  main()
finally:
  inputs.release()
  DISPLAY.destroy()
  print("Closed Everything. END")
#End
