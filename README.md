# chess-robot  
  
For the Android/GUI version see the instructions in the versiongui directory.
    
3D printed chess robot, Python code for Raspberry Pi, other Linux or Windows PC. New users should use version 2.

Install Stockfish engine, Python 3, python-pip, espeak

pip install pyserial  
pip install psutil  
pip install numpy  
pip install opencv-python  
pip install stockfish  
pip install pyttsx3  

Run CBint.py from Thonny or elsewhere.

The camera should be positioned directly over the centre of the chess board and lined up pretty well. Then camera calibration asks you to click on the four corners of the playing area of the chessboard (on the image), and you are shown the result. Click them in the order requested. (The robot arm should not be in the way, and all the pieces must be in their correct starting positions). By "playing area" we mean the chessboard squares, NOT including any external margin).

The calibration is remembered even if all systems are shut down, so if the robot, board and camera have not been moved, recalibration can optionally be avoided when a new game is started

The camera should be at least 56 cm above the board. Square size 3.4 cm. Tallest piece: 5.5 cm. The image of a piece should not fall across an adjacent square.

Calibrating the Cartesian robot arm: The lower strut must be vertical and the upper strut horizontal and coming out straight over the board.

Code configuration: You will need to check squaresize, axistorow8, etc. in robotmove.py. Check the declarations in CBstate.py.

Axistorow8 is the distance in mm horizontally along the y coordinate, between the robot’s vertical axis and the centre of row 8. 


The RPi or PC is connected to the Arduino by a USB A/B cable (printer cable). Or alternatively via Bluetooth (not BLE), using an HC-05 Bluetooth module.

Both USB and IP cameras are supported. Calibration for fish-eye distortion is provided, and is more likely to be needed for IP cameras. USB cameras are often OK without it.
  
===  
Version 1 only:  
pip install pillow  
On RPi install fswebcam, aplay

