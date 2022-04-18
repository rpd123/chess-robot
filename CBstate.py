import os
import platform
cbstate = ""

if platform.system() == "Windows":
    windowsos = True
    mydir = r'C:\Users\Richard\chessreal4\images' + "\\"
    stockfishexe = r'C:\Program Files\Stockfish\stockfish.exe'
    cameraportno = 1
    cameraportno = 0
    #cameraportno = 'http://192.168.1.189:8080/video'
    serialport = "COM3"
else:
    windowsos = False
    mydir = "/home/pi/chessreal4/images/"
    serialport = '/dev/ttyACM0'

