#!/usr/bin/python3
#serialTest.py
import serial
import time

WAITTIME=1
serName="/dev/ttyAMA0"
ser = serial.Serial(serName)
print (ser.name)
print (ser)
if ser.isOpen():
  try:
    print("For Serial Loopback - connect GPIO Pin8 and Pin10")
    print("[Type Message and Press Enter to continue]")
    print("#:")
    command=input()
    ser.write(bytearray(command+"\r\n","ascii"))
    time.sleep(WAITTIME)
    out=""
    while ser.inWaiting() > 0:
      out += bytes.decode(ser.read(1))
    if out != "":
      print (">>" + out)
    else:
      print ("No data Received")
  except KeyboardInterrupt:
    ser.close()
#End

