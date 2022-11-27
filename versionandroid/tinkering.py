from tkinter import *

def image_clicked(event):
    print ("an image on the canvas was clicked!")
    print ("now opening xml file...")
    #todo: open xml file here
    print(event.x, event.y)
root = Tk()

canvas = Canvas(root, width=500, height=500)
canvas.pack()

canvas.create_rectangle([0,0,100,100], fill="blue", tag="opens_xml")
canvas.tag_bind("opens_xml", "<1>", image_clicked)

root.mainloop()