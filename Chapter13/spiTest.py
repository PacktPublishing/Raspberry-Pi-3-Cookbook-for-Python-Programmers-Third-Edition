#!/usr/bin/python3
# spiTest.py
import wiringpi

print("Add SPI Loopback - connect GPIO Pin19 and Pin21")
print("[Press Enter to continue]")
input()
wiringpi.wiringPiSPISetup(1,500000)
buffer=str.encode("HELLO")
print("Buffer sent %s" % buffer)
wiringpi.wiringPiSPIDataRW(1,buffer)
print("Buffer received %s" % buffer)
print("Remove the SPI Loopback")
print("[Press Enter to continue]")
input()
buffer=str.encode("HELLO")
print("Buffer sent %s" % buffer)
wiringpi.wiringPiSPIDataRW(1,buffer)
print("Buffer received %s" % buffer)
#End
