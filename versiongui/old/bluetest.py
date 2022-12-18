'''
import socket

adapter_addr = 'e4:a4:71:63:e1:69'
adapter_addr = '98:d3:61:f6:76:e3'
adapter_addr = '26:3b:43:f0:f9:74'
port = 5  # Normal port for rfcomm?
buf_size = 1024

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((adapter_addr, port))
s.listen(1)
try:
    print('Listening for connection...')
    client, address = s.accept()
    print(f'Connected to {address}')

    while True:
        data = client.recv(buf_size)
        if data:
            print(data)
except Exception as e:
    print(f'Something went wrong: {e}')
    client.close()
    s.close()
'''   
    
"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket

serverMACAddress = '00:1f:e1:dd:08:3d'
serverMACAddress = '98:d3:61:f6:76:e3'
serverMACAddress = '26:3b:43:f0:f9:74'
port = 4
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()
'''
import bluetooth

target_name = "HC-05"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
 if target_name == bluetooth.lookup_name( bdaddr ):
    target_address = bdaddr
    break

if target_address is not None:
  print ("found target bluetooth device with address ", target_address)
else:
  print ("could not find target bluetooth device nearby")
  '''