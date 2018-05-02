#!/usr/bin/python3
#log_local.py
import time
import datetime
import data_adc as dataDevice

DEBUG=True
FILE=True
VAL0=0;VAL1=1;VAL2=2;VAL3=3 #Set data order
FORMATHEADER="\t%s\t%s\t%s\t%s\t%s"
FORMATBODY="%d\t%s\t%f\t%f\t%f\t%f"

if(FILE):f = open("data.log",'w')
def timestamp():
  ts=time.time() 
  return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def main():
    counter=0
    myData = dataDevice.device()
    myDataNames=myData.getName()
    header=(FORMATHEADER%("Time",myDataNames[VAL0],myDataNames[VAL1],myDataNames[VAL2],myDataNames[VAL3]))
    if(DEBUG):print (header)
    if(FILE):f.write(header+"\n")
    while(1):
      data=myData.getNew()
      counter+=1
      body=(FORMATBODY%(counter,timestamp(),data[0],data[1],data[2],data[3]))
      if(DEBUG):print (body)
      if(FILE):f.write(body+"\n")
      time.sleep(0.1)

try:
  main()
finally:
  f.close()
#end
