#!/usr/bin/env python
#
# This module copyright 2018, 2022 Richard Day, chess@gotobiz.co.uk
# This code must not be resold, or redistributed in any way without express permission


import CBstate 
mydir = CBstate.mydir
if CBstate.windowsos:
    import pyttsx3

from subprocess import call                         

import time     # import the time library for the sleep function
from math import sin, cos, atan2

import serial
try:
    sp = serial.Serial(CBstate.serialport, 9600, timeout=1)
    sp.reset_input_buffer()
except:
    print("No serial port")

time.sleep(1)

axistorow8 = 96  # mm
servoonleft = True
#squaresize = 31    # mm
squaresize = 35 # mm
gripperfloatheight = 60
grippergrabheight = -25 
gripperoffset = 26
openamount = 37 #degrees
closeamount = 0 #degrees
graveyard = "i6"

xmtrans = {
    "a": 3.5,
    "b": 2.5,
    "c": 1.5,
    "d": 0.5,
    "e": -0.5,
    "f": -1.5,
    "g": -2.5,
    "h": -3.5,
    "i": -4.5,
    "j": -5.5
}

xtrans = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9
}
#pieceheights = {
#   "p": 3.2,   # cm
#   "r": 3.6,
#   "n": 3.2,   # grab lower
#   "b": 4.9,
#   "q": 5.7,
#   "k": 6.3
#}
pieceheights = {
    "p": 2.7,   # cm
    "r": 3.0,
    "n": 3.2,   # grab lower
    "b": 4.1,   # 
    "q": 4.6,   # 
    "k": 5.3    # grab lower
}
maxpieceheight = 2.5    # inches

piecewidths = {
    "p": 0,     # degrees
    "r": 3,
    "n": 0,
    "b": 3,
    "q": 4,
    "k": 4
}

gameresult = ("No result", "Checkmate! White wins", "Checkmate! Black wins", "Stalemate", "50 moves rule", "3 repetitions rule")
lastmovetype = (
    "Normal",
    "En passant available",
    "Capture en passant",
    "Pawn promoted",
    "Castle on king's side",
    "Castle on queen's side")

firsttime = 1

def waiter(dur):
    time.sleep(dur)

def movearmcoord (xmm, ymm, zmm):
    #print ((xmm, ymm, zmm))
    adjymmint = int(ymm)+axistorow8
    theta = atan2(adjymmint, int(xmm))
    adjxmm = str(int(round(int(xmm) - (gripperoffset*cos(theta)))))
    adjymm = str(int(round(adjymmint - (gripperoffset*sin(theta)))))
    
    gstring = "G1" + " X" + adjxmm + " Y" + adjymm + " Z" + str(zmm) + "\r"
    #print (gstring)
    #input("Check G-codes then press enter")
    sp.flush()
    sp.write(gstring.encode())
    line=sp.read_until().decode('utf-8').rstrip()
    print(line)
    #input("press enter")

def opengripper(amount):
    adjamount = amount
    if servoonleft:
        adjamount = 90 - amount
    mycode = "M5 T" + str(adjamount) + "\r"
    sp.flush()
    sp.write(mycode.encode())
    waiter(1)

def closegripper(amount, piecetype):
    adjamount = amount + piecewidths[piecetype]
    if servoonleft:
        adjamount = 90 - (adjamount)
    mycode = "M3 T" + str(adjamount) + "\r"
    sp.flush()
    sp.write(mycode.encode())
    waiter(1)

def speaker(text):
    if CBstate.windowsos:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        cmd_beg= 'espeak -s100 '
        cmd_end= ' | aplay ' + mydir + 'Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
        cmd_out= '--stdout >' + mydir + 'Text.wav ' # To store the voice file
        text = text.replace(' ', '_')
        call([cmd_beg+cmd_out+text], shell=True)
        call(["aplay", mydir + "Text.wav"])

    
def quitter():
    print ("reset all steppers")
    sp.flush()
    sp.write(("M18" + "\r").encode()) 
    print ("Game ends")
    time.sleep(3)
    sp.close()
    quit()

def pickuppiece(xmm, ymm, piecetype):
    global pieceheights
    opengripper(openamount)
    print("go down to pick up")
    movearmcoord (xmm, ymm, grippergrabheight + (pieceheights[piecetype]*10))  # go down half way
    waiter(2)
    movearmcoord (xmm, ymm, grippergrabheight)  # go down
    closegripper(closeamount, piecetype)
    #waiter(1)
    print("go up")
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def droppiece(xmm, ymm):
    
    print("go down to drop piece")
    movearmcoord (xmm, ymm, grippergrabheight)  # go down
    opengripper(openamount)
    #waiter(1)
    print("go up")
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def takepiece (xmm, ymm, targetpiece):
    movearmcoord (xmm, ymm, gripperfloatheight)
    pickuppiece(xmm,ymm, targetpiece)
    gravex = (xmtrans[graveyard[0]] * squaresize)-10
    gravey = (8-int(graveyard[1])) * squaresize
    movearmcoord (gravex, gravey, gripperfloatheight)
    droppiece(gravex, gravey)
    gohome()

def iscastling (sourcesquarename):
    
    if CBstate.cbstate == 4:
        rsourcexmm = xmtrans["h"] * squaresize
        rsourceymm = (8-int("8")) * squaresize
        rtargetxmm = xmtrans["f"] * squaresize
        rtargetymm = (8-int("8")) * squaresize
    elif CBstate.cbstate == 5:
        rsourcexmm = xmtrans["a"] * squaresize
        rsourceymm = (8-int("8")) * squaresize
        rtargetxmm = xmtrans["d"] * squaresize
        rtargetymm = (8-int("8")) * squaresize
    else:
        return()
    print("Castling " + sourcesquarename)   
    movearmcoord (rsourcexmm, rsourceymm, gripperfloatheight)
    
    pickuppiece(rsourcexmm, rsourceymm, "r")
    movearmcoord (rtargetxmm, rtargetymm, gripperfloatheight)
    droppiece(rtargetxmm, rtargetymm,)
    opengripper(openamount)
    print("go up")
    movearmcoord (rtargetxmm, rtargetymm, gripperfloatheight)
    gohome()
    
def enpassant (sourcesquarename):
    if CBstate.cbstate == 2:
        epsquarename = sourcesquarename[0:1] + str(int(sourcesquarename[1:2]) - 1)
        print (epsquarename)
        epxmm = xmtrans[epsquarename[0:1]] * squaresize
        epymm = (8 - int(epsquarename[1:2])) * squaresize
        takepiece(epxmm, epymm, epsquarename)


def updateboard(source, target, boardbefore):
    # called from CBint
    sourcex = xtrans[source[0]]
    sourcey = 8-int(source[1])
    targetx = xtrans[target[0]]
    targety = 8-int(target[1])
    print (boardbefore)
    boardbefore[targety][targetx] = boardbefore[sourcey][sourcex] 
    boardbefore[sourcey][sourcex] = "." 
    print (boardbefore) 
    return (boardbefore)

def movepiece (sourcesquarename, targetsquarename, boardbefore):
    # called from CBint 
    sourcexmm = xmtrans[sourcesquarename[0:1]] * squaresize
    sourceymm = (8 - int(sourcesquarename[1:2])) * squaresize
    
    targetxmm = xmtrans[targetsquarename[0:1]] * squaresize
    targetymm = (8 - int(targetsquarename[1:2])) * squaresize
    
    # for board:
    sourcex = xtrans[sourcesquarename[0]]
    sourcey = 8-int(sourcesquarename[1])
    targetx = xtrans[targetsquarename[0]]
    targety = 8-int(targetsquarename[1])
    
    if boardbefore[targety][targetx] != ".":        # row, column
        #print (boardbefore)
        print("Take piece!")
        takepiece(targetxmm, targetymm, boardbefore[targety][targetx].lower())      
    print ("sourcex= ", sourcex)
    
    movearmcoord (sourcexmm, sourceymm, gripperfloatheight)
    opengripper(openamount)
    #input("now pick up:")
    sourcepiece = boardbefore[sourcey][sourcex].lower()
    print("sourcepiece " + sourcepiece)
    
    movearmcoord (sourcexmm, sourceymm, grippergrabheight)
    closegripper(closeamount, sourcepiece)
    movearmcoord (sourcexmm, sourceymm, gripperfloatheight)
    #input("now move piece to target. Enter:") 
    movearmcoord (targetxmm, targetymm, gripperfloatheight)
    #input("now drop:")
    movearmcoord (targetxmm, targetymm, grippergrabheight)
    opengripper(openamount)     
    #input("now go up:")
    print("go up")
    movearmcoord (targetxmm, targetymm, gripperfloatheight)
    print("go home")
    gohome()
    
    iscastling(sourcesquarename)
    enpassant (sourcesquarename)

def calibrategripper():
    while True:
        angle = input("Provide angle in degrees, or q:")
        if angle == "q":
            quitter()
        opengripper(angle)
        #waiter(1)
def gohome():
    movearmcoord (0, -10+gripperoffset, 180)

def init():
    try:
        print ("Start") 
        line=sp.readline().decode('utf-8').rstrip()
        print(line)
        line=sp.readline().decode('utf-8').rstrip()
        print(line)
        calirob = input("Calibrate robot? y/n")
        if calirob == "y":
            #time.sleep(1)
            sp.write(("G28" + "\r").encode())
        input("Press Enter to switch on steppers")
        sp.write(("M17" + "\r").encode())
        input("Press Enter to continue!")
        gohome()
        
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        quitter()   
    
    

#init()  # testing
