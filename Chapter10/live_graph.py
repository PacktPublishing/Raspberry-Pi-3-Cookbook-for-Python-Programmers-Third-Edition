#!/usr/bin/python3
#live_graph.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import data_local as dataDevice

PADDING=5
myData = dataDevice.device()
dispdata = []
timeplot=0
fig, ax = plt.subplots()
line, = ax.plot(dispdata)

def update(data):
  global dispdata,timeplot
  timeplot+=1
  dispdata.append(data)
  ax.set_xlim(0, timeplot)
  ymin = min(dispdata)-PADDING
  ymax = max(dispdata)+PADDING
  ax.set_ylim(ymin, ymax)
  line.set_data(range(timeplot),dispdata)
  return line

def data_gen():
  while True:
    yield myData.getNew()[1]/1000

ani = animation.FuncAnimation(fig, update, 
                              data_gen, interval=1000)
plt.show()
#End