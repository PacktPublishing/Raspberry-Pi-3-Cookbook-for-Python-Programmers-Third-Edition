#!/usr/bin/env python3
#data_local.py
import subprocess
from random import randint
import time

MEM_TOTAL=0
MEM_USED=1
MEM_FREE=2
MEM_OFFSET=7
DRIVE_USED=0
DRIVE_FREE=1
DRIVE_OFFSET=9
DEBUG=False
DATANAME=["CPU_Load","System_Temp","CPU_Frequency",
          "Random","RAM_Total","RAM_Used","RAM_Free",
          "Drive_Used","Drive_Free"]

def read_loadavg():
  # function to read 1 minute load average from system uptime
  value = subprocess.check_output(
            ["awk '{print $1}' /proc/loadavg"], shell=True)
  return float(value)

def read_systemp():
  # function to read current system temperature
  value = subprocess.check_output(
            ["cat /sys/class/thermal/thermal_zone0/temp"],
            shell=True)
  return int(value)

def read_cpu():
  # function to read current clock frequency
  value = subprocess.check_output(
            ["cat /sys/devices/system/cpu/cpu0/cpufreq/"+
             "scaling_cur_freq"], shell=True)
  return int(value)
  
def read_rnd():
  return randint(0,255)

def read_mem():
  # function to read RAM info
  value = subprocess.check_output(["free"], shell=True)
  memory=[]
  for val in value.split()[MEM_TOTAL+
                           MEM_OFFSET:MEM_FREE+
                           MEM_OFFSET+1]:
    memory.append(int(val))
  return(memory)
  
def read_drive():
  # function to read drive info
  value = subprocess.check_output(["df"], shell=True)
  memory=[]
  for val in value.split()[DRIVE_USED+
                           DRIVE_OFFSET:DRIVE_FREE+
                           DRIVE_OFFSET+1]:
    memory.append(int(val))
  return(memory)

class device:
  # Constructor:
  def __init__(self,addr=0):
    self.NAME=DATANAME
    
  def getName(self):
    return self.NAME

  def getNew(self):
    data=[]
    data.append(read_loadavg())
    data.append(read_systemp())
    data.append(read_cpu())
    data.append(read_rnd())
    memory_ram = read_mem()
    data.append(memory_ram[MEM_TOTAL])
    data.append(memory_ram[MEM_USED])
    data.append(memory_ram[MEM_FREE])
    memory_drive = read_drive()
    data.append(memory_drive[DRIVE_USED])
    data.append(memory_drive[DRIVE_FREE])
    return data

def main():
  LOCAL = device()
  print (str(LOCAL.getName()))
  for i in range(10):
    dataValues = LOCAL.getNew()
    print (str(dataValues))
    time.sleep(1)

if __name__=='__main__':
  main()
#End