# Vision code

# This module copyright 2018 Richard Day, chess@gotobiz.co.uk
# This code must not be resold, or distributed in any way without express permission

# For each square compute standard deviation and mean of colour values within the square
# Can tell which squares are empty by standard deviation being below a certain value
# After which we distinguish between black (brown) and white because max mean for brown is less than min mean for white

import time 
import os
import cv2
import sys
import numpy
#import psutil
#from PIL import Image
import CBstate
mydir = CBstate.mydir
import logging

firsttimeonly = 1
firstgbp = 1
splitwb = 112
splitwbonb = 112
splitwbonw = 112
stdrgb = 23
#squaring = 1 # number of times to look at squaring image

img_dimension = 319 
pts_src = numpy.array([[100, 100], [100, 100], [100, 100],[100, 100]])
pts8 = [0,0,0,0,0,0,0,0]
whereclick = ["top left", "bottom left", "top right", "bottom right"]
pointscount = 0

xrevtrans = {
    1: "a",
    2: "b",
    3: "c",
    4: "d",
    5: "e",
    6: "f",
    7: "g",
    8: "h"
}

# Now initialize board arrays
xx, yy = 8, 8;
pieces = [["e" for x in range(xx)] for y in range(yy)]
oldpieces = [["e" for x in range(xx)] for y in range(yy)]
for row in range(2):
    for col in range(8):
        pieces[row][col] = "b"
        oldpieces[row][col] = "b"
for row in range(6,8):
    for col in range(8):
        pieces[row][col] = "w"
        oldpieces[row][col] = "w"   

def updateforcomputermove(board):
    global oldpieces, pieces, firsttimeonly
    if firsttimeonly:
        firsttimeonly = 0
        print ("first time only:")      
    
    else:
        for x in range(8):
            for y in range(8):
                current = board[x][y]
                if current == ".":
                    oldpieces[x][y] = "e"
                elif current.islower():
                    oldpieces[x][y] = "b"
                else:
                    oldpieces[x][y] = "w"
    print ("After computer move:")
    print (oldpieces)
    #raw_input("Now any key")
            
def drawredlines():
    #im = Image.open(mydir + '4.jpg', 'r')
    im = cv2.imread(mydir + '4.jpg')
    #pix = im.load()
    
    h, w, c = im.shape
    squaresizex = float(w)/8   
    squaresizex = int(round(squaresizex))
    squaresizey = float(h)/8
    squaresizey = int(round(squaresizey))
    
    i = 0
    while i < w:
        j = 0
        while j < h:
            im[i,j] = (0,0,255)
            j += 1
        i += squaresizex
    j = 0
    while j < h:
        i = 0
        while i < w:
            im[i,j] = (0,0,255)
            i += 1
        j += squaresizey
    #im.save(mydir + 'redlines.jpg')  # Save the modified pixels
    #im = Image.open(mydir + 'redlines.jpg', 'r')
    #im.show()   # uncomment to test
    cv2.imwrite(mydir + "redlines.jpg", im)
    cv2.imshow("Red Lines", im)
    print("Press any key to continue")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def dummymove(board):
    global firstgbp
    while True:
        firstgbp = 1
        getplayermove (board, ()) # dummy in order to get best number to differentiate between black and white
        #drawredlines()       
        return()    # comment out for testing
        conti = input("Try again? y/n")
        if conti == "n":
            return()
        
def undistort():
    img = cv2.imread(mydir + "1.jpg")
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(CBstate.K, CBstate.D, numpy.eye(3), CBstate.K, CBstate.DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite(mydir + "1.jpg", undistorted_img)
    #cv2.imshow("Undistorted", undistorted_img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def takepiccv2():
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
        #cv2.imshow('preview',frame)
        #time.sleep(3)
        print (mydir + "1.jpg")
        if CBstate.scale_percent != 100:
            width = int(frame.shape[1] * CBstate.scale_percent / 100)
            height = int(frame.shape[0] * CBstate.scale_percent / 100)
            dim = (width, height)  
            # resize image
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)        
        cv2.imwrite(mydir + "1.jpg", frame)
        if CBstate.fisheye:
            undistort()
            
    finally:
        vc.release()
        cv2.destroyAllWindows()

def takepic():
    print ("Take picture ...")
    if True:
        takepiccv2()
    else:   
        os.system('fswebcam -r 640x480 -S 20 --set "Power Line Frequency"="50 Hz" --no-banner --delay 2 --set brightness=25% --jpeg 50 --save ' + mydir + '1.jpg')  
        #os.system('fswebcam -r 640x480 -S 5 -F 5 --set "Power Line Frequency"="50 Hz" --list-controls --no-banner --delay 1 --set brightness=50% --set "Exposure, Auto"=False --set "Exposure (absolute)"=400 --jpeg 50 --save /home/pi/stepperchessrpd/images/1.jpg')

def homog():
    global pts_src
    # read points file
    pss = [0,0,0,0,0,0,0,0]  # declare
    f = open(mydir + 'points.txt', 'r')
    try:
        pointscurr = f.readline().rstrip()
        print(pointscurr)
        pointscurrsplit = pointscurr.split(",")
        # split points file
        for i in range(8):
            pss[i] = int(pointscurrsplit[i])             
    finally:        
        f.close()
    
    im_src = cv2.imread(mydir + "1.jpg", 1)
    pts_src = numpy.array([[pss[0],pss[1]],[pss[2],pss[3]],[pss[4],pss[5]],[pss[6],pss[7]]])
    # Four corners in destination image.
    pts_dst = numpy.array([[0,0],[0,img_dimension],[img_dimension,0],[img_dimension, img_dimension]])

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    #im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
    im_out = cv2.warpPerspective(im_src, h, (img_dimension+1, img_dimension+1))
    if CBstate.rotation != -1:
        im_out = cv2.rotate(im_out, CBstate.rotation)    
    cv2.imwrite(mydir + "4.jpg", im_out)
    image = cv2.rotate(im_out, cv2.ROTATE_90_COUNTERCLOCKWISE)    
    #cv2.imshow("Straightened Image", image)   
    #cv2.waitKey(0)

# function to display the coordinates of
# of the points clicked on the image

def click_event(event, x, y, flags, params):
    global pointscount, pts_src, im_src, pts8
    
    # checking for left mouse clicks    
    if event == cv2.EVENT_LBUTTONDOWN:                  
        
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        pts_src [pointscount] = [x,y]
        pts8[pointscount*2] = x
        pts8[(pointscount*2)+1] = y
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im_src, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', im_src)
        pointscount += 1
        if pointscount == 4:
            print (pts_src)
            # save points to file
            f = open(mydir + 'points.txt', 'w')
            try:
                forjoin = ["0","0","0","0","0","0","0","0"]
                for i in range(8):
                    forjoin[i] = str(pts8[i])
                    
                joined = ",".join(forjoin)
                f.write(joined)
            finally:        
                f.close()
                print ("Press any key to continue")
            return() 
        else:
            print ("Now click " + whereclick[pointscount])
            
def calibratecamera(board):
    global firstgbp, im_src, pointscount, pts8
    takepic()
    
    while True:
        pointscount = 0
        pts8 = [0,0,0,0,0,0,0,0]
        print ("Click the four corners of the PLAYING AREA, starting with top left")
        im_src = cv2.imread(mydir + "1.jpg", 1)

        cv2.imshow('image', im_src)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('image', click_event)

        # wait for a key to be pressed to exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #cv2.waitKey(1)
        im_src = cv2.imread(mydir + "1.jpg", 1)
        #im_dst = cv2.imread(mydir + '4.jpg')
        # Four corners in destination image.
        pts_dst = numpy.array([[0,0],[0,img_dimension],[img_dimension,0],[img_dimension, img_dimension]])

        # Calculate Homography
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image to destination based on homography
        #im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
        im_out = cv2.warpPerspective(im_src, h, (img_dimension+1, img_dimension+1))
        if CBstate.rotation != -1:
            im_out = cv2.rotate(im_out, CBstate.rotation)
        cv2.imwrite(mydir + "4.jpg", im_out)
        #print ("Press any key to continue")
        cv2.imshow("Straightened Image", im_out)
        print ("White should be on left of Straightened Image")
        print ("Press any key to continue")
        cv2.waitKey(0)
            
        cv2.destroyAllWindows()
        
        tryagain = input ("Try again (y/n)?")
        if tryagain =="n":
            break
    print ("Finished straightening")
        
    drawredlines()
    return

def newcastling(board, validkingmoves):
    global pieces
    print ("castling code")
    #print (pieces)
    print (validkingmoves)
    if board[7][4] == "K" :
        print ("h1")
        for (i, j) in validkingmoves:
            tup = (i, j)
            print ("h2", tup)
            if tup == (6,7):
                print ("h3")
                if pieces [7][4] == "e" and pieces[7][5] != "e" and pieces[7][6] != "e" and pieces [7][7] == "e" :
                    print ("castled king side")
                    return ("me1g1")
            if tup == (2,7):
                if pieces [7][0] == "e" and pieces[7][1] == "e" and pieces[7][2] != "e" and pieces [7][3] != "e" and pieces[7][4] == "e" :
                    print ("castled queen side")
                    return ("me1c1")
        # code for invalid castling:
        # on king's side, if K..R before and (6,7) not in validkingmoves and pieces ewwe then invalid castling
        if (6,7) not in validkingmoves:
            if board[7][4:8] == "K..R":
                if pieces[7][4:8] == "ewwe":
                    print ("Invalid: castled king side")
                    return ("me1g1")
        # on queen's side, if R...K before and (2,7) not in validkingmoves and pieces eewwe then invalid castling
        if (2,7) not in validkingmoves:
            if board[7][0:5] == "R...K":
                if pieces[7][0:5] == "eewwe":
                    print ("Invalid: castled queen side")
                    return ("me1g1")
        return ("")
    
def castling(board, validkingmoves):
    global pieces
    print ("castling code")
    #print (pieces)
    print (validkingmoves)
    if board[7][4] == "K" :
        print ("h1")
        #piecesr = list(zip(*reversed(pieces)))  # rotate
        for (i, j) in validkingmoves:
            tup = (i, j)
            print ("h2", tup)
            if tup == (6,7):
                print ("h3")
                if pieces [7][4] == "e" and pieces[7][5] != "e" and pieces[7][6] != "e" and pieces [7][7] == "e" :
                    print ("castled king side")
                    return ("me1g1")
            if tup == (2,7):
                if pieces [7][0] == "e" and pieces[7][1] == "e" and pieces[7][2] != "e" and pieces [7][3] != "e" and pieces[7][4] == "e" :
                    print ("castled queen side")
                    return ("me1c1")
        return ("")
        
def enpassantmove (board):
    global pieces
    if CBstate.cbstate == 1:    # piece available for en passant
        a = 1
                
def getplayermove(board, validkingmoves):
    global pieces, oldpieces, firstgbp, splitwb, splitwbonb, splitwbonw, stdrgb
    updateforcomputermove(board)
    print ("Take pic ...")
    if True:
        takepiccv2()
    else:
        os.system('fswebcam -r 640x480 -S 20 --set "Power Line Frequency"="50 Hz" --no-banner --delay 2 --set brightness=25% --set "Exposure, Auto Priority"=False --jpeg 50 --save ' + mydir + '1.jpg')
        #os.system('fswebcam -r 640x480 -S 5 -F 5 --set "Power Line Frequency"="50 Hz" --list-controls --no-banner --delay 1 --set brightness=50% --set "Exposure, Auto"=False --set "Exposure (absolute)"=400 --jpeg 50 --save /home/pi/stepperchessrpd/images/1.jpg')
    #takepic()
    ###im = Image.open(mydir + '1.jpg', 'r')
    #im = im.rotate(90, expand=True)  
    ###crop(im)
    #nudgecrop(im)
   
    homog()
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    pix = cv2.imread(mydir + '4.jpg')
        
    h, w, c = pix.shape
    squaresizex = float(w)/8   
    squaresizex = int(round(squaresizex))
    squaresizey = float(h)/8
    squaresizey = int(round(squaresizey))
    
    minRw = minRe = minRb = minGw = minGe = minGb = minBw = minBe = minBb = 256
    minRwonw = minRwonb = minGwonb = minBwonw = 256
    maxRwonw = maxRbonb = 0
    
    maxRw = maxRe = maxRb = maxGw = maxGe = maxGb = maxBw = maxBe = maxBb = 0
    maxRbonb = maxRbonw = 0
    
    minstdp = 256
    maxstde = 0
    
    fudge = 9
    for row in range(8):    
        for col in range(8):
            i = int((row * squaresizex) + fudge)        
            pixlistR = []
            pixlistG = []
            pixlistB = []
            pixlisteR = []
            pixlisteG = []
            pixlisteB = []
            pixlistoR = []
            pixlistoG = []
            pixlistoB = []
            while i < ((row + 1) * squaresizex) - fudge:
                j = int((col * squaresizey) + fudge)
                            
                while j < ((col + 1) * squaresizey) - fudge:
                    pixlistB.append (pix[j,i][0])
                    pixlistG.append (pix[j,i][1])
                    pixlistR.append (pix[j,i][2])
                    if ((i+j) % 2) == 0:    #even
                        pixlisteB.append (pix[j,i][0])
                        pixlisteG.append (pix[j,i][1])
                        pixlisteR.append (pix[j,i][2])
                    else:
                        pixlistoB.append (pix[j,i][0])
                        pixlistoG.append (pix[j,i][1])
                        pixlistoR.append (pix[j,i][2])
                    j += 1
                i += 1

            stdR = numpy.std(pixlistR)
            stdG = numpy.std(pixlistG)
            stdB = numpy.std(pixlistB)
            #print (stdR)
            #print (stdG)
            #print (stdB)
            #todebug = str(row) +" " + str(col) +" " + " std: " + str(stdR) +" " + str(stdG) +" " + str(stdB)
            #logging.debug (todebug)
            #print("mean:")
            meanR = numpy.mean(pixlistR)
            meanG = numpy.mean(pixlistG)
            meanB = numpy.mean(pixlistB)
            if ((row+col) % 2) == 0:    #even
                meanRe = numpy.mean(pixlisteR)
                meanGe = numpy.mean(pixlisteG)
                meanBe = numpy.mean(pixlisteB)
            else:
                meanRo = numpy.mean(pixlistoR)
                meanGo = numpy.mean(pixlistoG)
                meanBo = numpy.mean(pixlistoB)
            #print (meanR)
            #print (meanG)
            #print (meanB)
            #print("next")
            if firstgbp:
                if ((row+col) % 2) == 0:    #even
                    todebug = str(row) +" " + str(col) +" " + " meansRGBe: " + str(meanRe) +" " + str(meanGe) +" " + str(meanBe)
                    logging.debug (todebug)
                else:
                    todebug = str(row) +" " + str(col) +" " + " meansRGBo: " + str(meanRo) +" " + str(meanGo) +" " + str(meanBo)
                    logging.debug (todebug)
                if row < 2:
                    minRw = min (minRw, meanR) #
                    if ((row+col) % 2) == 0:    #even
                        minRwonb = min(minRwonb, meanRe)
                    else:
                        minRwonw = min(minRwonw, meanRo)
                        #maxRwonw = max(maxRwonw, meanBo)
                    maxRw = max (maxRw, meanR)
                    minGw = min (minGw, meanG)
                    maxGw = max (maxGw, meanG)
                    minBw = min (minBw, meanB)
                    maxBw = max (maxBw, meanB)
                    minstdp = min (minstdp, stdR + stdG + stdB)
                elif row >5:
                    minRb = min (minRb, meanR)
                    maxRb = max (maxRb, meanR) #
                    if ((row+col) % 2) == 0:    #even
                        maxRbonb = max(maxRbonb, meanRe)
                    else:
                        maxRbonw = max(maxRbonw, meanRo)
                    minGb = min (minGb, meanG)
                    maxGb = max (maxGb, meanG)
                    minBb = min (minBb, meanB)
                    maxBb = max (maxBb, meanB)
                    minstdp = min (minstdp, stdR + stdG + stdB)
                else:
                    minRe = min (minRe, meanR)
                    maxRe = max (maxRe, meanR)
                    minGe = min (minGe, meanG)
                    maxGe = max (maxGe, meanG)
                    minBe = min (minBe, meanB)
                    maxBe = max (maxBe, meanB)
                    maxstde = max (maxstde, stdR + stdG + stdB)
                # Not all of above assigned min and max variables are currently subsequently used :-)
            
            if stdR + stdG + stdB < stdrgb:
                pieces [7-row][col] = "e"
                logging.debug ("empty")
            else:
                #if meanR + meanG + meanB < 250:
                #if meanR + meanG + meanB < splitwb :
                '''
                if meanR < splitwb :
                    pieces [7-row][col] = "b"
                    logging.debug ("black " + meanR)
                else: 
                    pieces [7-row][col] = "w"
                    logging.debug ("white " + meanR)
                ''' 
                if ((row+col) % 2) == 0:    #even
                    if meanRe < splitwbonb :
                        pieces [7-row][col] = "b"
                        logging.debug ("black %s", meanRe)
                    else: 
                        pieces [7-row][col] = "w"
                        logging.debug ("white %s", meanRe)
                else:   
                    if meanRo < splitwbonw :
                        pieces [7-row][col] = "b"
                        logging.debug ("black %s", meanRo)
                    else: 
                        pieces [7-row][col] = "w"
                        logging.debug ("white %s", meanRo)
                
    #print (minRw, maxRw, minGw, maxGw, minBw, maxBw)
    #print (minRe, maxRe, minGe, maxGe, minBe, maxBe)
    #print (minRb, maxRb, minGb, maxGb, minBb, maxBb)
    #print ("minRw: ", minRw, ", maxRb: ", maxRb) 
    #print ("minGw: ", minGw, ", maxGb: ", maxGb) 
    #print ("minBw: ", minBw, ", maxBb: ", maxBb) 
    if firstgbp :
        splitwb = (minRw + maxRb)/2
        #splitwbonw = (minRwonw + maxRbonw) / 2
        splitwbonw = (minRwonw + maxRbonw) / 2
        splitwbonb = (minRwonb + maxRbonb) / 2
        
        print ("splitwb: ", splitwb)
        print ("splitwbonw: ", splitwbonw)
        print ("splitwbonb: ", splitwbonb)
        print("minRwonb, minRwonw, maxRbonb, maxRbonw", minRwonb, minRwonw, maxRbonb, maxRbonw)
        print("maxRwonw", maxRwonw)
        print ("minstdp, maxstde", minstdp, maxstde)
        stdrgb = (minstdp + maxstde) / 2
        print ("stdrgb", stdrgb)
        #input("Enter")
    print ("meanRe", meanRe)
    print ("meanRo", meanRo)
    
    #splitwb = (minRw + minGw + minBw + maxRb + maxGb + maxBb) / 2  
    #splitwb = ((minRw + minGw + minBw) * 2/3) + ((maxRb + maxGb + maxBb) / 3)              
    #print (minRw + minGw + minBw)
    #print (maxRb + maxGb + maxBb)
    
    constructmove = list("m    ")
    for row in range(8):    
        for col in range(8):

            if oldpieces[row][col] == "w" and pieces[row][col] == "e":
                constructmove[1] =  xrevtrans[col+1]
                constructmove[2] =  str(8-row)
            if  (oldpieces[row][col] == "e" and pieces[row][col] != "e") or \
                (oldpieces[row][col] == "b" and pieces[row][col] == "w") :
                constructmove[3] =  xrevtrans[col+1]
                constructmove[4] =  str(8-row)  
            #print ("m", oldpieces[row][col], pieces[row][col])
            if not firstgbp :               
                oldpieces[row][col] = pieces[row][col] # new to old
            else:               
                pieces[row][col] = oldpieces[row][col] # old to new, first (dummy) time 
    
    #print (oldpieces)
    print (pieces)  

    movestr = ''.join(constructmove)
    castles =  castling(board, validkingmoves)
    if castles :
        movestr = castles
    else:
        movestr = ''.join(constructmove)        
    print (movestr)
    firstgbp = 0
    sys.stdout.flush()
    return (movestr)

