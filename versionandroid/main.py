import CBstate
mydir = CBstate.mydir

import CBint
import cv2
import time
import kivy
kivy.require("1.11.1")
#from kivy.config import Config
#Config.set('graphics', 'width', '1100')
#Config.set('graphics', 'height', '2280')
print(kivy.__version__)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.modalview import ModalView
from kivy.graphics import *
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

#Config.set('graphics', 'height', '780')
#Config.set('graphics', 'height', '2280')
from kivy.core.window import Window
Window.size = (640, 960)

# Huawei 1920 x 1080 pixels
# R-P screen 720 x 1480
#HP Webcam 2300 720 x 1280
#Windows 1280 x 720

from functools import partial
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.camera import Camera
#from kivy.config import Config

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    spacing: 0
''')

import playermove_rpd as RDpm

class P(RelativeLayout):
    pass

class Image(Image):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
        

        self.start_pos = [0, 0]
        self.end_pos = [0, 0]
        self.img_path = mydir+'1.jpg'
        
       
    def dispop(self, myx, myy):
    #def show_popup():
        #global pointscount
        view = ModalView(auto_dismiss=True,
                         size_hint=(None,None),
                         size=(160, 46),
                         pos_hint={'x': 320 / Window.width, 
                            'y':320 /  Window.height},
                         #pos = (320, 940)
                         )
        wherenext = "\nWhat now?"
        if RDpm.pointscount < 3:
            wherenext = "\nNow click " + RDpm.whereclick[RDpm.pointscount+1]
            
        vbutton = Button(
            text="[" + str(myx) + ", " + str(myy) + "]" + wherenext,
            size=(150,22),
            #text_size  = self.size,
            size_hint =(None, None),
            #halign = "left",
            #pos =(myx, myy),
            background_color=(0, 0, 0, 0))
        view.add_widget(vbutton)
        
        view.open()
        return view
    
    def hidethebutton(self, abutton, *args):
        abutton.text=""
        
    def on_touch_down(self, touch):
        #global mytext
        #rect_size = [10, 10]
        #if self.root.ids.myimage.collide_point(*touch.pos):
        if self.collide_point(*touch.pos):    
            with self.canvas:
                #self.canvas.clear()

                #self.size = (320, 320)
                self.end_pos = [round(touch.x,2), round(touch.y,2)]
                print("End pos  :", self.end_pos)
                mytext = str(self.end_pos)
                print (mytext)
                #show_popup()
                view = self.dispop(round(touch.x,2), round(touch.y,2))
                
                hstate = RDpm.registerclicks(int(round(touch.x)), int(round(512-touch.y)))
                #vcallback = self.hidethebutton(vbutton)
                #Clock.schedule_once(partial(self.hidethebutton, vbutton), 0.75)
                view.dismiss()
                if hstate == "finished":

                    #self.root.ids.animg.source = mydir+'4.jpg'
                    #self.root.ids.animg.reload()
                    self.size = (360, 360)
                    self.source = mydir+'redlines.jpg'
                    self.reload()
                    #App.get_running_app().stop()
        else:
            print ("Don't click here!")
class TouchApp(App):
   
        
    def capture(self, btn):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        #Parent.ids['myimg'] = self.img        
        
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png(mydir+"1.png")
        print("Image captured")        

        aimg = cv2.imread(mydir+'1.png')
        cv2.imwrite(mydir+'1.jpg', aimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        self.img.source = mydir+'1.jpg'
        self.img.reload()
        #self.remove_widget(self.camera)
        #self.remove_widget(btn)
        
    def startgame(self, startbtn):
        self.toplabel.text = "Starting game"
        print("Starting game")
        RDpm.dummymove(CBint.chessboard.getBoard())
        self.toplabel.text = "Game started"
        print ("Game started")
        
    def startrobot (self, startrobotbtn):
        self.toplabel.text = "Starting robot"
        print("Starting robot")
        if CBint.robotinit():
            self.toplabel.text = "Robot started"
            print("Robot started")
        else:
           self.toplabel.text = "Error: no serial port"
           print("Error: no serial port") 
        
    def playerhasmoved(self, movebtn):
        self.toplabel.text = "Player has moved"
        print("Player has moved")
        CBint.getboard()
        CBint.fbmove()
        self.toplabel.text = CBint.toplabel
    def cameraclick(self, Parent):
        pass

    
    def clear_canvas(self,obj):
        self.ROI.canvas.clear()
        
    def carryon(self):        
        print ("boo")
        
        return self.img

    def validate_input(self, window, key, *args, **kwargs):
        textfield = self.root.ids.textfield
        if key == 13 and textfield.focus: # The exact code-key and only the desired `TextInput` instance.
#           textfield.do_undo() # Uncomment if you want to strip out the new line.
            textfield.focus = False
            self.root.ids.lbl.text = textfield.text
#           textfield.text = "" # Uncomment if you want to make the field empty.
            print(textfield.text)
            #self.remove_widget(self.ids['_button'])
            print ("boo")
            #canvas.clear()

            #self.carryon()
            return True
    
    def build(self):
        
        Window.bind(on_keyboard = self.validate_input)        
           
        Parent = BoxLayout(orientation='vertical',
                           #minimum_height = '8000dp'
                           )
        
        self.toplabel = Label(
            text="Let's play chess!",
            size_hint= (1.0, None),
            height= 30,
            #width = 300
            )
        Parent.ids['toplbl'] = self.toplabel
        Parent.add_widget(self.toplabel)
        '''        
        mylabel = Label(
            text='Calibrate camera?',
            size_hint= (None, None),
            height= 30,
            width = 120
            )
        Parent.ids['lbl'] = mylabel
        Parent.add_widget(mylabel)
        
        btny = Button(
            text = 'Yes',
            size_hint = (None, None),
            height = '30dp',
            width = '60dp',
            on_press = self.cal
            )
        Parent.add_widget(btny)
        '''
        ##
        '''
        mytextinput = TextInput(
            hint_text = "Enter text here",
            size_hint= (20, None),
            height= 30,
            multiline= False
            )
        Parent.ids['textfield'] = mytextinput
        Parent.add_widget(mytextinput)
        
       
        #but = Button(text="clear", size_hint_x=0.2)
        #but.bind(on_release=self.clear_canvas)
        #Parent.add_widget(but)
        #self.load_kv("overlay.kv")
        #self.cameraclick(Parent)
        '''
        
        self.camera = Camera(
            resolution = CBstate.cameraresolution,
            #resolution = (640, 311),
            index = CBstate.cameraportno,
            play = True
            )
        
        self.btn = Button(
            text = 'Calibrate chessboard?',
            size_hint_y = None,
            height = '48dp',
            on_press = self.capture
            )
        
        #self.btn.bind(on_press = self.capture)
        #self.capture(self.btn)
        Parent.add_widget(self.camera)
        Parent.add_widget(self.btn)
        # end camera
        
        #self.ROI = TouchInput()
        #Parent.add_widget(self.ROI)
        
                # Load Image
        self.img_path = 'images/1.jpg'
        self.img = Image(source=self.img_path)
        self.img.allow_stretch = True
        self.img.keep_ratio = True
        self.img.size = (640, 360)
        self.img.pos = (0, 0)
        self.img.opacity = 1

        Parent.add_widget(self.img)
        Parent.ids['animg'] = self.img
        
        self.startbtn = Button(
            text = 'Start Game',
            size_hint_y = None,
            height = '48dp',
            on_press = self.startgame
            )
        Parent.add_widget(self.startbtn)
        
        self.startrobotbtn = Button(
            text = "Start robot",
            size_hint_y = None,
            height = '48dp',
            on_press = self.startrobot
            )
        Parent.add_widget(self.startrobotbtn)
        
        self.movebtn = Button(
            text = "I've moved!",
            size_hint_y = None,
            height = '48dp',
            on_press = self.playerhasmoved
            )
        Parent.add_widget(self.movebtn)
        
        return Parent

#import CBint
if __name__ == "__main__":
    TouchApp().run()
    
print ("Finished")
