# chess-robot
3D printed chess robot, Raspberry Pi code

Install Stockfish engine, Python 3, python-pip

On RPi install espeak, aplay and fswebcam

pip install pyserial

pip install psutil

pip install numpy

pip install pillow

pip install opencv-python

pip install stockfish

pip install pyttsx3


Run CBint.py from Thonny

The camera should be positioned directly over the centre of the chess board and lined up pretty well. Then camera calibration asks you to click on the four corners of the playing area of the chessboard (on the image), and you are shown the result. (The robot arm should not be in the way).

The calibration is remembered even if all systems are shut down, so if the robot, board and camera have not been moved, recalibration can optionally be avoided when a new game is started

The camera should be at least 56 cm above the board. Square size 3.5 cm. Tallest piece: 5.3 cm.

Calibrating the robot arm: The lower strut must be vertical and the upper strut horizontal and coming out straight over the board.

Code configuration: You will need to check squaresize, axistorow8, etc. in robotmove.py. Check the declarations in CBstate.py.

Axistorow8 is the distance in mm horizontally along the y coordinate, between the robot’s vertical axis and the centre of row 8. 
