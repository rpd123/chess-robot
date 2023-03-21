# Take pictures for fisheye calibration
import cv2
import time
import sys
import platform
import CBstate

imgno = 0

def takepic(imgno):
    #cv2.namedWindow("preview")
    try:
        if CBstate.windowsos:
            if CBstate.cameratype == 'usb':
                vc = cv2.VideoCapture(CBstate.cameraportno, cv2.CAP_DSHOW)
            else:
                vc = cv2.VideoCapture(CBstate.cameraportno, cv2.CAP_FFMPEG)
        else:
            vc = cv2.VideoCapture(CBstate.cameraportno)

        if vc.isOpened(): # try to get the first frame
            ret, frame = vc.read()
        else:
            print ("Failed to access camera")
            time.sleep(1)
            sys.exit()
        cv2.imshow('preview',frame)
        cv2.waitKey()
        print (CBstate.fisheyeimages + str(imgno) + ".jpg")
        if CBstate.scale_percent != 100:
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)  
            # resize image
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
        cv2.imwrite(CBstate.fisheyeimages + str(imgno) +  ".jpg", frame)
    finally:
        vc.release()
        cv2.destroyAllWindows()

while True:
    conti = input("Take a pic? y/n")
    if conti == "y":
        imgno += 1
        takepic(imgno)
    else:
        print ("Finished")
        sys.exit()
    
    