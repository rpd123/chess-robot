import CBstate
mydir = CBstate.mydir

import CBint
import cv2
#import time
import kivy
kivy.require("1.11.1")
#from kivy.config import Config
#Config.set('graphics', 'width', '1100')
#Config.set('graphics', 'height', '2280')
print(kivy.__version__)
from kivy.app import App
#from kivy.uix.widget import Widget
#from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.modalview import ModalView
from kivy.graphics import *
#from kivy.clock import Clock
#from kivy.uix.textinput import TextInput

#Config.set('graphics', 'height', '780')
#Config.set('graphics', 'height', '2280')
from kivy.core.window import Window
Window.size = CBstate.windowsize

#from functools import partial
#from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.camera import Camera
#from kivy.config import Config

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    spacing: 0
''')
import robotmove as RD
import playermove_rpd as RDpm
#import bluerpd.py
class P(RelativeLayout):
    pass

class MyImage(Image):
    def __init__(self, **kwargs):
        super(MyImage, self).__init__(**kwargs)
        

        #self.start_pos = [0, 0]
        #self.end_pos = [0, 0]
        #self.img_path = mydir+'1.jpg'
        
       
    def dispop(self, myx, myy):
    #def show_popup():
        #global pointscount
        '''
        view = ModalView(auto_dismiss=True,
                         size_hint=(None,None),
                         size=(160, 46),
                         pos_hint={'x': 320 / Window.width, 
                            'y':320 /  Window.height},
                         #pos = (320, 940)
                         )
        '''
        wherenext = ""
        if RDpm.pointscount < 3:
            wherenext = "Now click " + RDpm.whereclick[RDpm.pointscount+1]
        self.parent.ids.toplbl.text = "[" + str(myx) + ", " + str(myy) + "]. " + wherenext
        '''
        vbutton = Button(
            text="[" + str(myx) + ", " + str(myy) + "]" + "\n" + wherenext,
            size=(150,22),
            #text_size  = self.size,
            size_hint =(None, None),
            #halign = "left",
            #pos =(myx, myy),
            background_color=(0, 0, 0, 0))
        view.add_widget(vbutton)
        
        view.open()
        '''
        return
    
    def hidethebutton(self, abutton, *args):
        abutton.text=""
        
    def on_touch_down(self, touch):
        #global mytext
        #rect_size = [10, 10]
        if self.parent.ids.animg.collide_point(*touch.pos):
        #if self.collide_point(*touch.pos):    
            with self.canvas:
                #self.canvas.clear()
                print(self.to_local(touch.x, touch.y, True))
                mydim = int(round(self.parent.ids.animg.size[1]))
                print ("dimensions:")
                print (self.parent.ids.animg.size[0], self.parent.ids.animg.size[1], self.parent.ids.animg.texture_size[0], self.parent.ids.animg.texture_size[1])
                #self.size = (320, 320)
                #self.end_pos = [round(touch.x,2), round(touch.y,2)]
                #print("End pos  :", self.end_pos)
                #mytext = str(self.end_pos)
                #print (mytext)
                #show_popup()
                print ("loc:")
                localisedxy = self.to_local(int(round(touch.x)), int(round(touch.y)), True)
                print(localisedxy)
                self.dispop(localisedxy[0], int(round(mydim - localisedxy[1])))
                ############## Note reveral of y
                #self.parent.ids.toplbl.text = "img height= " + str(self.parent.ids.animg.height)
                #mydim = self.parent.ids.animg.norm_image_size[1]
                
                #mydim = self.parent.ids.animg.texture_size[1]
                
                imgdim = self.parent.ids.animg.texture_size[1]
                RDpm.update_img_dimension(imgdim)
                
                #expander = int(mydim/self.parent.ids.animg.texture_size[0])
                #expanderx = int(expander * CBstate.windowsize[0])
                #expandery = int(expander * CBstate.windowsize[1])
                reductionfactor = imgdim/self.parent.ids.animg.size[1]
                print ("red:")
                print (reductionfactor)
                hstate = RDpm.registerclicks(int(round(localisedxy[0] * reductionfactor)), int(round((mydim - localisedxy[1]) * reductionfactor)))
                #vcallback = self.hidethebutton(vbutton)
                #Clock.schedule_once(partial(self.hidethebutton, vbutton), 0.75)
                if hstate == "finished":
                    #view.dismiss()
                
                    self.parent.ids.toplbl.text = "If OK with white on left then start game"
                    #self.root.ids.animg.source = mydir+'4.jpg'
                    #self.root.ids.animg.reload()
                    
                    print ("img height= " + str(self.parent.ids.animg.height))
                    self.size = (mydim, mydim)
                    self.source = mydir+'redlines.jpg'
                    self.reload()
                    #App.get_running_app().stop()
        else:
            print ("[outside]")
class TouchApp(App):
   
    firstmove = 1
    ccount = 0
    
    def capture(self, btn):
        '''
        Capture the image
        '''
        #Parent.ids['myimg'] = self.img
        self.img.width = CBstate.windowsize[0]
        toptext = "Image captured. Click on bottom left of board below."
        if btn.text == "I've moved!":
            toptext = "Board image captured"
        
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        #self.camera.export_to_png(mydir+"1.png")
        self.camera.texture.save(mydir+"1.png")
        print("Image captured")        
        self.toplabel.text = toptext
        aimg = cv2.imread(mydir+'1.png')
        cv2.imwrite(mydir+'1.jpg', aimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        self.img.source = mydir+'1.jpg'
        self.img.reload()
        #self.remove_widget(self.camera)
        #self.remove_widget(btn)        
        
    def startgame(self, startbtn):
        #self.startrobotbtn.text = RD.startrobotbtntext1
        CBint.fnewgame()
        self.capture(startbtn)            
        imgdim = self.img.texture_size[1]
        RDpm.update_img_dimension(imgdim)        
        
        self.toplabel.text = "Starting game"
        print("Starting game")
        RDpm.dummymove(CBint.chessboard.getBoard())
        self.toplabel.text = "Game started. Start robot"
        print ("Game started")
        
    def startrobot (self, startrobotbtn):
        if self.startrobotbtn.text == RD.startrobotbtntext1:            
            print("Starting robot")
            if CBint.robotinit():
                
                self.toplabel.text = RD.toplabeltext2
                self.startrobotbtn.text = RD.startrobotbtntext2
                print(RD.toplabeltext2)
                #CBint.getboard()
                #CBint.fbmove()
            else:
                self.toplabel.text = "Error: no serial port"
                print("Error: no serial port")
        elif self.startrobotbtn.text == RD.startrobotbtntext2:
            
            RD.init2()# switch on steppers
            self.startrobotbtn.text = RD.startrobotbtntext3
            self.toplabel.text = RD.toplabeltext3
            
            print(RD.toplabeltext3)
        elif self.startrobotbtn.text == RD.startrobotbtntext3:
            RD.gohome()
            self.toplabel.text = RD.toplabeltext4
            self.startrobotbtn.text = RD.startrobotbtntext1
            print(RD.toplabeltext4)
        else:
            print ("Error 17")
            
    def showredlines(self):
        ##
        mydim = int(round(self.img.size[1]))
        self.img.size = (mydim, mydim)
        self.img.source = mydir+'redlines.jpg'
        self.img.reload()        
        ##
        
    def playerhasmoved(self, movebtn):
        self.capture(movebtn)
        ##
        self.showredlines()        
        ##
        if self.firstmove:
            self.firstmove = 0
            #Start the clock
            #Clock.schedule_interval(self.Callback_Clock, 2)
        
        self.toplabel.text = "Player has moved "
        print("Player has moved")
        print (CBint.toplabel)
        self.toplabel.text += CBint.toplabel
        #CBint.getboard()
        CBint.fbmove()
        print (CBint.toplabel)
        self.capture(movebtn)               
        ##
        self.showredlines()        
        ##
        self.toplabel.text = "Computer move: " + CBint.toplabel 
    def Callback_Clock(self, dt):
        self.ccount = self.ccount+1
        print ("Updated %d...times"%self.count)
        RD.receivemsg(sp)
        
    def cameraclick(self, Parent):
        self.orientation = 'vertical'
           
    def clear_canvas(self,obj):
        self.ROI.canvas.clear()
        
    def carryon(self):        
        print ("boo")
        
        return self.img

    def validate_input(self, window, key, *args, **kwargs):
        textfield = self.parent.ids.textfield
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
        
        #Window.bind(on_keyboard = self.validate_input)        
           
        Parent = BoxLayout(orientation='vertical',
                           #minimum_height = '8000dp'
                           )
        
        self.toplabel = Label(
            text="Let's play chess!",
            size_hint= (1.0, None),
            font_size = '14sp',
            height= '34dp',
            #width = 300
            )
               
        Parent.ids['toplbl'] = self.toplabel
        Parent.add_widget(self.toplabel)
      
        self.camera = Camera(
            #resolution = CBstate.cameraresolution,
            #resolution = (640, 311),
            #resolution = (960, 540),
            allow_stretch = True,
            keep_ratio = True,
            #height = CBstate.cameraheight,
            size_hint = (0.75,0.75),
            #width = CBstate.windowsize[0], 
            index = CBstate.cameraportno,
            play = True
            )
        Parent.add_widget(self.camera)
        self.btn = Button(
            text = 'Calibrate chessboard?',
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.capture
            )
        
        #self.btn.bind(on_press = self.capture)
        #self.capture(self.btn)
        
        Parent.add_widget(self.btn)
        # end camera
        
        #self.ROI = TouchInput()
        #Parent.add_widget(self.ROI)
        
                # Load Image
        self.img = MyImage(
            #source=mydir + '1.jpg',
            allow_stretch = True,
            nocache=True,
            keep_ratio = True,
            width = CBstate.windowsize[0],            
            size_hint_x = (None),
            opacity = 1
            )
        Parent.add_widget(self.img)
        Parent.ids['animg'] = self.img
        
        self.startbtn = Button(
            text = 'New game',
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.startgame
            )
        Parent.add_widget(self.startbtn)
        
        self.startrobotbtn = Button(
            text = RD.startrobotbtntext1,
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.startrobot
            )
        Parent.add_widget(self.startrobotbtn)
        
        self.movebtn = Button(
            text = "I've moved!",
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.playerhasmoved
            )
        Parent.add_widget(self.movebtn)
        
        return Parent

#import CBint
if __name__ == "__main__":
    TouchApp().run()
    
print ("Finished")
