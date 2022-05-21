import os
import platform
import logging

cbstate = ""

scale_percent = 100 # percent of original size, if required to make original image smaller to fit screen

# white should be on left of Straightened Image
rotation = -1   # do not rotate
#rotation = 0  #cv2.ROTATE_90_CLOCKWISE 
#rotation = 1  #cv2.ROTATE_180
#rotation = 2  #cv2.ROTATE_90_COUNTERCLOCKWISE

if platform.system() == "Windows":
    windowsos = True
    mydir = r'C:\Users\Richard\chessreal4\images' + "\\"
    stockfishexe = r'C:\Program Files\Stockfish\stockfish.exe'
    cameraportno = 1
    #cameraportno = 0
    #cameraportno = 'http://192.168.1.189:8080/video'
    #cameraportno = 'rtsp://tapoadmin:tapoadmin@192.168.1.127:554/stream1'
    cameratype = 'usb'
    #cameratype = 'ip'
    serialport = "COM4"
else:
    windowsos = False
    mydir = "/home/pi/chessreal4/images/"
    cameraportno = 0
    serialport = '/dev/ttyACM0'
    
logging.basicConfig(level=logging.DEBUG, filename = mydir + 'chesslog.log', filemode='w', format='%(levelname)s-%(message)s')
