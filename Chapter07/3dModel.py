#!/usr/bin/python3
""" Wavefront obj model loading. Material properties set in
    mtl file. Uses the import pi3d method to load *everything*
"""
import demo
import pi3d
from math import sin, cos, radians

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()
# Fetch key presses
inputs=pi3d.InputEvents()
    
def main():
  #Model textures and shaders
  shader = pi3d.Shader("uv_reflect")
  bumptex = pi3d.Texture("textures/floor_nm.jpg")
  shinetex = pi3d.Texture("textures/stars.jpg")
  # load model
  mymodel = pi3d.Model(file_string='models/teapot.obj', z=10)
  mymodel.set_shader(shader)
  mymodel.set_normal_shine(bumptex, 4.0, shinetex, 0.5)

  #Create environment box
  flatsh = pi3d.Shader("uv_flat")
  ectex=pi3d.loadECfiles("textures/ecubes","sbox")
  myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES",
                                 name="cube")
  myecube.set_draw_details(flatsh, ectex)
    
  CAMERA = pi3d.Camera.instance()
  rot = 0.0 # rotation of camera
  tilt = 0.0 # tilt of camera
    
  while DISPLAY.loop_running() and not \
                               inputs.key_state("KEY_ESC"):
    #Rotate camera
    inputs.do_input_events()
    # camera steered by mouse
    #Note:Some mice devices will be located on
    #get_mouse_movement(1) instead of get_mouse_movement()
    mx,my,mv,mh,md=inputs.get_mouse_movement()
    #mx,my,mv,mh,md=inputs.get_mouse_movement(1)
    rot -= (mx)*0.2
    tilt -= (my)*0.2
    CAMERA.reset()
    CAMERA.rotate(tilt, rot, 0)
    #Rotate object
    mymodel.rotateIncY(2.0)
    mymodel.rotateIncZ(0.1)
    mymodel.rotateIncX(0.3)
    #Draw objects
    mymodel.draw()
    myecube.draw()

try:
  main()
finally:
  inputs.release()
  DISPLAY.destroy()
  print("Closed Everything. END")
#End
