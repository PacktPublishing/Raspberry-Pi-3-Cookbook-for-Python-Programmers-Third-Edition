#!/usr/bin/python3
#serialMenu.py
import time
import RPi.GPIO as GPIO
import serialControl as SC
SERNAME = "/dev/ttyUSB0"
running=True

CMD=0;PIN=1;STATE=2;OFF=0;ON=1
GPIO_PINS=[7,11,12,13,15,16,18,22]
GPIO_STATE=["OFF","ON"]
EXIT="EXIT"

def gpioSetup():
  GPIO.setmode(GPIO.BOARD)
  for pin in GPIO_PINS:
    GPIO.setup(pin,GPIO.OUT)

def handleCmd(cmd):
  global running
  commands=cmd.upper()
  commands=commands.split()
  valid=False
  print ("Received: "+ str(commands))
  if len(commands)==3:
    if commands[CMD]=="GPIO":
      for pin in GPIO_PINS:
        if str(pin)==commands[PIN]:
          print ("GPIO pin is valid")
          if GPIO_STATE[OFF]==commands[STATE]:
            print ("Switch GPIO %s %s"% (commands[PIN],
                                         commands[STATE]))
            GPIO.output(pin,OFF)
            valid=True
          elif GPIO_STATE[ON]==commands[STATE]:
            print ("Switch GPIO %s %s"% (commands[PIN],
                                         commands[STATE]))
            GPIO.output(pin,ON)
            valid=True
  elif commands[CMD]==EXIT:
    print("Exit")
    valid=True
    running=False
  if valid==False:
    print ("Received command is invalid")
    response="  Invalid:GPIO Pin#(%s) %s\r\n"% (
                      str(GPIO_PINS), str(GPIO_STATE))
  else:
    response="  OK\r\n"
  return (response)

def main():
  try:
    gpioSetup()
    with SC.serPort(serName=SERNAME) as mySerialPort:
      mySerialPort.send("\r\n")
      mySerialPort.send("  GPIO Serial Control\r\n")
      mySerialPort.send("  -------------------\r\n")
      mySerialPort.send("  CMD PIN STATE "+
                        "[GPIO Pin# ON]\r\n")
      while running==True:
        print ("Waiting for command...")
        mySerialPort.send(">>")
        cmd = mySerialPort.receive(terminate="\r\n")
        response=handleCmd(cmd)
        mySerialPort.send(response)
      mySerialPort.send("  Finished!\r\n")
  except OSError:
    print ("Check selected port is valid: %s" %serName)
  except KeyboardInterrupt:
    print ("Finished")
  finally:
    GPIO.cleanup()

main()
#End
