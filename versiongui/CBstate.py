import os
import platform
import logging
import numpy

cbstate = ""

scale_percent = 100 # percent of original size, if required to make original image smaller to fit screen

# white should be on left of Straightened Image
rotation = -1   # do not rotate
#rotation = 0  #cv2.ROTATE_90_CLOCKWISE 
rotation = 1  #cv2.ROTATE_180
#rotation = 2  #cv2.ROTATE_90_COUNTERCLOCKWISE
mirrorimage = False
if platform.system() == "Windows":
    windowsos = True
    mydir = r'C:\Users\Richard\Github\chess-robot\versiongui\images' + "\\"
    stockfishexe = r'C:\Program Files\Stockfish\stockfish.exe'
    cameraportno = 1
    cameraportno = 0
    #cameraportno = 'http://192.168.1.189:8080/video'
    #cameraportno = 'http://192.168.1.177:4747/video'
    #cameraportno = 'rtsp://tapoadmin:tapoadmin@192.168.1.127:554/stream1'
    cameratype = 'usb'
    #cameratype = 'ip'
    serialport = "COM3"
    cameraresolution = (1280,720)
    windowsize  = (cameraresolution[0]/2, 960)
    stockfishparams={"Threads": 4}
else:
    windowsos = False
    #mydir = "/media/sf_GitHub/chess-robot/version2/images/"
    chessenginepath = '/usr/games/stockfish'
    mydir = "images/"
    cameraportno = 0
    serialport = '/dev/ttyACM0'
    #serialport = '/dev/ttyS0'
    #serialport = '/dev/rfcomm0'
    cameraresolution = (640, 480)
    #windowsize = cameraresolution
    windowsize = (1080, 1920)
    windowsize = (720, 1280)  #Moto G (2nd Gen)
    #windowsize = (1440, 2560) # Galaxy S7
# Huawei P10 Lite (1080, 1920)
# R-P screen (720, 1480)
#HP Webcam 2300 (720, 1280)
#straightenedimagedimension = 0
#cameraheight = 520
sunfishengine = False

if 'ANDROID_STORAGE' in os.environ:
    print("Android!")
    androidos = True    
    bluetoothdevicename = 'HC-05'   # should match device in Settings...Bluetooth    
    chessenginepath = "/data/app/ccc.chess.engine.stockfish-1/lib/arm/libstockfish15.so"
    #chessenginepath = "/data/app/ccc.chess.engine.stockfish-1/lib/arm64/libstockfish15.so"
    depth = 10
    #stockfishparams={"Slow Mover": 50}
    mirrorimage = True
else:
    androidos = False
    
if sunfishengine:
    #import sys
    #myfish = r'C:\Users\Richard\Github\chess-robot\versionsunfish\sunfish.py'
    myfish = "sunfish.py"
    #chessenginepath = "['"+sys.executable + "', '" + myfish+"']"
    #print (stockfishenginepath)
    depth = 5

movetime = "10000"     #Chess engine time to move in milliseconds
slowmover = "50"

motorsareservos = False
SCARA = False
steppergripper = True

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