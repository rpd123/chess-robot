#!/usr/bin/env python
#
# This module copyright 2018, 2022 Richard Day, chess@gotobiz.co.uk
# This code must not be resold, or redistributed in any way without express permission


import CBstate 
mydir = CBstate.mydir
import inversekinematics
import sys
if not CBstate.androidos:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 125) # Decrease the Speed Rate
else:
    import bluetrpd
    from plyer import tts
from subprocess import call                         
#import time     # import the time library for the sleep function
from math import sin, cos, atan2, sqrt, atan

import serial
#import bluetoothrpd
axistorow8 = 96  # mm
servoonleft = True
#squaresize = 31    # mm
squaresize = 35 # mm
gripperfloatheight = 60
grippergrabheight = -25 
gripperoffset = 26
openamount = 37 #degrees
closeamount = 2 #degrees
endstops = False
graveyard = "i6"
msgcount = 0

piecewidths = {
    "p": 0,     # degrees
    "r": 3,
    "n": 0,
    "b": 3,
    "q": 4,
    "k": 4
}

if CBstate.steppergripper:
    axistorow8 = 100  # mm
    servoonleft = True
    gripperfloatheight = 57
    grippergrabheight = -14 
    gripperoffset = 53
    openamount = 45 #degrees. Do not change
    closeamount = -55 #degrees
    
    piecewidths = {
        "p": 0,     # additional degrees
        "r": 3,
        "n": 0,
        "b": 3,
        "q": 4,
        "k": 4
    }
# end stepper gripper

if CBstate.SCARA:
    debugrobot = False
    axistorow8 = 35
    gripperfloatheight = 40
    grippergrabheight = -15
    gripperfloatheight = 0  # was 20, do not change
    grippergrabheight = -83  # was -63
    halfway = (gripperfloatheight + grippergrabheight) / 2
    gripperoffset = 0  # indeed!
    openamount = 50 #degrees
    closeamount = 15 #degrees
    #shank1 = 140
    shank1 = 153.0
    shank2 = 161.0    # includes gripper offset
    totalarmlength = shank1 + shank2   # when straight
    elbow = 0
    oldelbow = 0

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

gameresult = ("No result", "Checkmate! White wins", "Checkmate! Black wins", "Stalemate", "50 moves rule", "3 repetitions rule")
lastmovetype = (
    "Normal",
    "En passant available",
    "Capture en passant",
    "Pawn promoted",
    "Castle on king's side",
    "Castle on queen's side")

startrobotbtntext1 = "Start robot"
startrobotbtntext2 = "Switch on steppers"
startrobotbtntext3 = "Adjust ROBOT BASE rotation, then click"

toplabeltext2 = "Steppers are off. Place robot in start position and then switch on steppers"
toplabeltext3 = "Steppers are on. Adjust ROBOT placement, then press button"
toplabeltext4 = "Make move, then press 'I've moved' button"

firsttime = 1
#gtoplabel = ""
sp = 0
send_stream = 0

def waiter(dur):
    #time.sleep(dur)
    pass

def delayarduino(dur):
    return
    gstring = "G4 " + str(dur)
    send_stream.write(gstring.encode())
    
def spflush():
    if CBstate.androidos:
        pass
    else:
        sp.flush()
        
def flushout():
    if CBstate.androidos:
        send_stream.flush()
    else:
        pass
    
def receivemsg(sp):
    global msgcount
    msgcount += 1
    line=""
    if CBstate.androidos:
        #bluetrpd.breceivemsg(sp)
        if sp.ready():
            line=sp.readLine()
            #line = line.decode('utf-8').rstrip() 
            #spflush()
    else:    
        #line=sp.readline().decode('utf-8').rstrip()
        line=sp.read_until().decode('utf-8').rstrip()
        spflush()
    print(msgcount, line)
    
def scaraviastraight(xmm, adjymmint, zmm):
    global elbow, oldelbow
    #print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
    oldelbow = elbow
    #print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
    if xmm > 0 and adjymmint < totalarmlength:
        elbow = 0
    
    if xmm > 135:   # parked
        elbow = 0
    
    if xmm < 0 and adjymmint < totalarmlength:
        elbow = 1

    if elbow != oldelbow:
        print ("elbow: " + str(elbow) + " oldelbow: " + str(oldelbow))
        #intermediate move to straight out
        gstring = "G1" + " X0" + " Y" + str(totalarmlength) + " Z" + str(zmm) + "\r"
        print (gstring)
        send_stream.write(gstring.encode())
        receivemsg(sp)
        #input("press enter")

def movearmcoord (xmm, ymm, zmm):  # zmm is height
    receivemsg(sp)
    adjymmint = int(ymm)+axistorow8
    theta = atan2(adjymmint, int(xmm))
    adjxmm = str(int(round(int(xmm) - (gripperoffset*cos(theta)))))   #gripperoffset 0 for SCARA
    adjymm = str(int(round(adjymmint - (gripperoffset*sin(theta)))))  #gripperoffset 0 for SCARA
    if CBstate.SCARA:
        armreach = sqrt((xmm*xmm) + (int(adjymmint)*int(adjymmint)))
        if armreach > totalarmlength:
            print ("Too far away! " + str(armreach))
        #print ((xmm, ymm, zmm))
        scaraviastraight(xmm, adjymmint, zmm)
        
    if CBstate.motorsareservos:
        # A 10 130 120 110 --> Moving the robot Arm with 10ms step time, 130º upper joint angle, 120º lower joint angle and 110º base rotator angle
        # length, height, angle, gripper, wrist angle, wrist rotate
        theangles = inversekinematics.inversekinematics(sqrt((adjxmm * adjxmm) + (adjymm * adjymm)), zmm, 90 + (rtod * (atan(x/y))), 0, -90, 0)
        #theangles: Shoulder, Elbow, Wrist, rotation, g, wr
        gstring = "A 10 " + theangles[1] + " " + theangles[0]  + " " + theangles[3] + theangles[2] + "\r"
        print (gstring)
    else:
        gstring = "G1" + " X" + adjxmm + " Y" + adjymm + " Z" + str(zmm) + "\r"
        print (gstring) ###
    #receivemsg(sp) ####
    #input("Check G-codes then press enter") ###
    spflush()
    #sp.reset_input_buffer()
    send_stream.write(gstring.encode())
    receivemsg(sp)
    #receivemsg(sp) ####
    #input("press enter")

def opengripper(amount):
    adjamount = amount
    if servoonleft:
        adjamount = 90 - amount
    if CBstate.motorsareservos:
        mycode = "G0\r"
    else:
        mycode = "M5 T" + str(adjamount) + "\r"
    print ("Open gripper")
    spflush()
    send_stream.write(mycode.encode())
    receivemsg(sp)
    waiter(0.5)

def closegripper(amount, piecetype):
    adjamount = amount + piecewidths[piecetype]
    if servoonleft:
        adjamount = 90 - (adjamount)
    if CBstate.motorsareservos:
        mycode = "G1\r"
    else:
        mycode = "M3 T" + str(adjamount) + "\r"
    print ("Close gripper")
    spflush()
    send_stream.write(mycode.encode())
    receivemsg(sp)
    #waiter(0.5)

def speaker(text):
    if CBstate.androidos:
        tts.speak(text)
    else:
        engine.setProperty('voice', 'english_rp+f3')
        engine.say(text)
        engine.runAndWait()
        return
        cmd_beg= 'espeak -ven+f4 -s100 '
        cmd_end= ' | aplay ' + mydir + 'Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
        cmd_out= '--stdout >' + mydir + 'Text.wav ' # To store the voice file
        text = text.replace(' ', '_')
        call([cmd_beg+cmd_out+text], shell=True)
        call(["aplay", mydir + "Text.wav"])

def quitter():
    global sp
    if sp:
        if CBstate.SCARA:
            gohome()
        #print ("reset all steppers")
        spflush()
        #send_stream.write(("M18" + "\r").encode())
        receivemsg(sp)
        #sp.close()               
        #time.sleep(2)
        print ("Game ends")
        speaker ("Game ends. Thankyou for playing.")
    if CBstate.androidos:
        gohome()
    else:
        engine.stop()
        sys.exit()
    return
    #quit()

def pickuppiece(xmm, ymm, piecetype):
    global pieceheights
    print ("open gripper")
    #opengripper(openamount)
    print("go down to pick up")
    movearmcoord (xmm, ymm, grippergrabheight + (pieceheights[piecetype]*10))  # go down half way
    #waiter(1)
    print (grippergrabheight)
    #input ("press enter")    
    movearmcoord (xmm, ymm, grippergrabheight) # go down
    delayarduino(5)
    #print("close gripper")
    closegripper(closeamount, piecetype)
    #waiter(1)
    delayarduino(5)
    print("go up")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def droppiece(xmm, ymm):
    
    print("go down to drop piece")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, grippergrabheight + 3)  # go down
    #print ("open gripper")
    delayarduino(5)
    opengripper(openamount)
    delayarduino(5)
    print("go up")
    #movearmcoord (xmm, ymm, halfway)
    movearmcoord (xmm, ymm, gripperfloatheight) # go up
    
def takepiece (xmm, ymm, targetpiece):
    speaker("Take piece.")
    movearmcoord (xmm, ymm, gripperfloatheight)
    pickuppiece(xmm,ymm, targetpiece)
    gravex = (xmtrans[graveyard[0]] * squaresize)-20
    gravey = (8-int(graveyard[1])) * squaresize
    movearmcoord (gravex, gravey, gripperfloatheight)
    droppiece(gravex, gravey)
    #input("press enter")
    #interx = xmtrans["h"] * squaresize
    #intery = (8-int("3")) * squaresize
    #movearmcoord (interx, intery, gripperfloatheight)
    #input("press enter")
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
        return
    print("Castling " + sourcesquarename)   
    movearmcoord (rsourcexmm, rsourceymm, gripperfloatheight)
    
    pickuppiece(rsourcexmm, rsourceymm, "r")
    movearmcoord (rtargetxmm, rtargetymm, gripperfloatheight)
    droppiece(rtargetxmm, rtargetymm,)
    opengripper(openamount)
    print("go up")
    movearmcoord (rtargetxmm, rtargetymm, gripperfloatheight)
    gohome()
    
def enpassant (targetxmm, targetymm):
    if CBstate.cbstate == 2:
        #epsquarename = targetsquarename[0:1] + str(int(targetsquarename[1:2]) + 1)
        #print (epsquarename)
        #epxmm = xmtrans[epsquarename[0:1]] * squaresize
        #epymm = (8 - int(epsquarename[1:2])) * squaresize
        takepiece(targetxmm, targetymm - squaresize, 'p') 

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
    sourcepiece = boardbefore[sourcey][sourcex].lower()
    print("sourcepiece " + sourcepiece)

    pickuppiece(sourcexmm, sourceymm, sourcepiece)
    #input("now move piece to target. Enter:")
    movearmcoord (targetxmm, targetymm, gripperfloatheight)

    droppiece(targetxmm, targetymm) 
    print("go home")
    gohome()
    
    iscastling(sourcesquarename)
    enpassant (targetxmm, targetymm) 

def calibrategripper():
    while True:
        angle = input("Provide angle in degrees, or q:")
        if angle == "q":
            quitter()
        opengripper(angle)
        #waiter(1)
def gohome():
    if CBstate.SCARA:
        #movearmcoord (313, 0, 0)  # xmm, ymm, zmm cartesian coordinates
        scaraviastraight(totalarmlength, 0, gripperfloatheight)
        #gstring = "G1" + " X" + str(shank1) + " Y" + str(shank2) + " Z" + str(gripperfloatheight) + "\r"
        gstring = "G1" + " X" + str(totalarmlength) + " Y0" + " Z" + str(gripperfloatheight) + "\r"
        waiter(1.2)
        print (gstring) ###
        #input("Check G-codes then press enter") ###
        spflush()
        #sp.reset_input_buffer()
        send_stream.write(gstring.encode())
        receivemsg(sp)
        #time.sleep(0.2)
        receivemsg(sp)
    else:
        movearmcoord (0, -30+gripperoffset, 180)

def initsteppers():
    #time.sleep(0.2)
    send_stream.write(("G28" + "\r").encode())   # steppers off, initialize
    #time.sleep(0.2)
    receivemsg(sp)
    #time.sleep(0.2)
    receivemsg(sp)
    
def steppers_on():
    #input("Then press Enter to switch on steppers")
    send_stream.write(("M17" + "\r").encode())   # Switch on steppers
    #time.sleep(0.2)
    receivemsg(sp)
    #time.sleep(0.2)
    receivemsg(sp)
'''    
def settop(t):
    t.text = "oooooh"
    print ("gtoplabel: " + t.text)
    time.sleep(10)
 '''   
def init():
    global sp, send_stream
    if sp:
        # re-calibrate robot
        sp.close()
        send_stream.close()
        sp = 0
        send_stream = 0

    if CBstate.androidos:
        sp, send_stream = bluetrpd.get_socket_stream(CBstate.bluetoothdevicename)
        '''
        try:
            #getDevname = self.the.config.get('bluetoothsettings', 'stringbluetdevname')
            sp, send_stream = bluerpd.get_port_connect('HC-05')
            return True
        except bluerpd.jnius.jnius.JavaException as e:
            print ('Not Connected')
            return False
           '''
    else:
        try:
            sp = serial.Serial(CBstate.serialport, 9600, timeout=2.0)
            send_stream = sp
            sp.reset_input_buffer()                
        except serial.SerialException as e:
            print("No serial port")
            print (e)
            #sp.close        
            quitter()
            return False
    #time.sleep(0.2)
    initsteppers()   # turn steppers off and initialize them
    try:
        print ("Start")        
        receivemsg(sp)
        receivemsg(sp)
        if endstops:
            pass
        else:
            print ("Calibrate robot now ...")
            
        return True
        #calirob = input("Calibrate robot manually? y/n")
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        quitter()
       
def init2():
    #initsteppers()   # turn steppers off and initialize them
    steppers_on()    # prompt user to switch on steppers

    if CBstate.SCARA:
        gohome()   # raises arm
        gstring = "G1" + " X0" + " Y" + str(totalarmlength) + " Z" + str(gripperfloatheight) + "\r"
        send_stream.write(gstring.encode())
        receivemsg(sp)
    else:
        movearmcoord (0, (squaresize*3.5), grippergrabheight)
    #input("Adjust ROBOT position slightly if not in centre of board. Press Enter to continue")
    #gohome()
    return True
                      
    #except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    #    quitter()   
    

#init()  # testing
