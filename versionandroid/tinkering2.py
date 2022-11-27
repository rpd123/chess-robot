#Import tkinter library
from tkinter import *
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
def callback(e):
   x= e.x
   y= e.y
   print("Pointer is currently at %d, %d" %(x,y))
win.bind('<Motion>',callback)
win.mainloop()