import os
import platform
import logging

cbstate = ""


if platform.system() == "Windows":
    windowsos = True
    mydir = r'C:\Users\Richard\chessreal4\images' + "\\"
    stockfishexe = r'C:\Program Files\Stockfish\stockfish.exe'
    cameraportno = 1
    #cameraportno = 0
    #cameraportno = 'http://192.168.1.189:8080/video'
    serialport = "COM4"
else:
    windowsos = False
    mydir = "/home/pi/chessreal4/images/"
    cameraportno = 0
    serialport = '/dev/ttyACM0'
    
logging.basicConfig(level=logging.DEBUG, filename = mydir + 'chesslog.log', filemode='w', format='%(levelname)s-%(message)s')
