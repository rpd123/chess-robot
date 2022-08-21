import os
import platform
import logging
import numpy

cbstate = ""

scale_percent = 100 # percent of original size, if required to make original image smaller to fit screen

# white should be on left of Straightened Image
rotation = -1   # do not rotate
#rotation = 0  #cv2.ROTATE_90_CLOCKWISE 
#rotation = 1  #cv2.ROTATE_180
#rotation = 2  #cv2.ROTATE_90_COUNTERCLOCKWISE

if platform.system() == "Windows":
    windowsos = True
    mydir = r'C:\Users\Richard\Github\chess-robot\version2\images' + "\\"
    stockfishexe = r'C:\Program Files\Stockfish\stockfish.exe'
    cameraportno = 1
    #cameraportno = 0
    #cameraportno = 'http://192.168.1.189:8080/video'
    #cameraportno = 'rtsp://tapoadmin:tapoadmin@192.168.1.127:554/stream1'
    cameratype = 'usb'
    #cameratype = 'ip'
    serialport = "COM3"    
else:
    windowsos = False
    #mydir = "/media/sf_GitHub/chess-robot/version2/images/"
    mydir = "images/"
    cameraportno = 0
    serialport = '/dev/ttyACM0'
    #serialport = '/dev/ttyS0'
    #serialport = '/dev/rfcomm0'
    
motorsareservos = False
SCARA = True

stockfishparams={"Threads": 4}

logging.basicConfig(level=logging.DEBUG, filename = mydir + 'chesslog.log', filemode='w', format='%(levelname)s-%(message)s')
kingincheck = False

fisheye = False
# Following for fisheye cameras only. Normally only for IP cameras
# You should replace these 3 lines with the output from calibrate_fisheye.py
# We provide the code from https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
# 3 lines below are for Tapo TC60
DIM=(1280, 720)
K=numpy.array([[817.2563502237226, 0.0, 623.8797454131019], [0.0, 817.8633343903235, 383.3817964461323], [0.0, 0.0, 1.0]])
D=numpy.array([[-0.15014017025387882], [1.3554015587876163], [-11.583862737184841], [29.439951469529348]])

fisheyeimages = "fishimages/"