import serial
import time
import sys

try:
    sp = serial.Serial("COM6", 9600, timeout=0.4)
    #sp.reset_input_buffer()                
except serial.SerialException as e:
    print("No serial port")
    print (e)
    sys.exit()
time.sleep(0.2)
print("Serial port opened")
