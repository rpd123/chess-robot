import cv2
import time
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.modalview import ModalView
from kivy.graphics import *
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.config import Config
Config.set('graphics', 'width', '1280')
#Config.set('graphics', 'height', '780')
Config.set('graphics', 'height', '2280')

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    spacing: 0
''')

mydir = "images/"
         
import homog

class fred():
    def freddy(a):
        print (a)
        return int(a)+10
class P(RelativeLayout):
    pass

class TouchInput(Widget):
    def __init__(self, **kwargs):
        super(TouchInput, self).__init__(**kwargs)
        

        self.start_pos = [0, 0]
        self.end_pos = [0, 0]
        self.img_path = 'images/1.jpg'
        
       
    def dispop(self, myx, myy):
    #def show_popup():
        #global pointscount
        view = ModalView(auto_dismiss=True,
                         size_hint=(None,None),
                         size=(150, 22),
                         #pos_hint ={'x':myx/640, 'y':myy/480},
                         pos = (320, 240)
                         )
        wherenext = "\nWhat now?"
        if homog.pointscount < 3:
            wherenext = "\nNow click " + homog.whereclick[homog.pointscount+1]
        view.add_widget(Button(
            text="[" + str(myx) + ", " + str(myy) + "]" + wherenext,
            size=(150,22),
            #text_size  = self.size,
            size_hint =(None, None),
            #halign = "left",
            #pos =(myx, myy),
            background_color=(0, 0, 0, 0)))
        
        view.open()
        return view
    def on_touch_up(self, touch):
        #global mytext
        rect_size = [10, 10]
        with self.canvas:
            self.canvas.clear()


            self.end_pos = [round(touch.x,2), round(touch.y,2)]
            print("End pos  :", self.end_pos)
            mytext = str(self.end_pos)
            print (mytext)
            #show_popup()
            view = self.dispop(round(touch.x,2), round(touch.y,2))
            
            hstate = homog.registerclicks(int(round(touch.x)), int(round(480-touch.y)))
            Clock.schedule_once(view.dismiss, 0.75)
            #view.dismiss()
            if hstate == "finished":
                App.get_running_app().stop()
class TouchApp(App):
   
        
    def capture(self, btn):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png(mydir+"5.png")
        print("Captured")        

        img = cv2.imread(mydir+'5.png')
        #cv2.imwrite(mydir+'5.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        
        #self.remove_widget(self.camera)
        #self.remove_widget(btn)
    
    def cameraclick(self, Parent):
        pass

    
    def clear_canvas(self,obj):
        self.ROI.canvas.clear()
        
    def carryon(self):        
        print ("boo")

    def validate_input(self, window, key, *args, **kwargs):
        textfield = self.root.ids.textfield
        if key == 13 and textfield.focus: # The exact code-key and only the desired `TextInput` instance.
#           textfield.do_undo() # Uncomment if you want to strip out the new line.
            textfield.focus = False
            self.root.ids.lbl.text = textfield.text
#           textfield.text = "" # Uncomment if you want to make the field empty.
            print(textfield.text)
            self.carryon()
            return True

    def build(self):
        
        Window.bind(on_keyboard = self.validate_input)
        return Builder.load_string(
"""
BoxLayout:
    #orientation: "vertical"
    
    spacing: "5dp"
    Label:
        id: lbl
        text:'Calibrate camera (y/n):'
    TextInput:
        id: textfield
        #multiline: False
        hint_text: "Enter text here"
""")
        #return True
        #Parent = BoxLayout(orientation='vertical')
        self.ROI = TouchInput()
        Parent.add_widget(self.ROI)
        #but = Button(text="clear", size_hint_x=0.2)
        #but.bind(on_release=self.clear_canvas)
        #Parent.add_widget(but)
        #self.load_kv("overlay.kv")
        #self.cameraclick(Parent)
        
        #camera
        
        self.camera = Camera(
            resolution = (1280,960),
            play = True
            )
        
        self.btn = Button(
            text = 'Capture',
            size_hint_y = None,
            height = '48dp',
            #on_press = self.capture
            )
        
        self.btn.bind(on_press = self.capture)
        self.capture(self.btn)
        Parent.add_widget(self.camera)
        Parent.add_widget(self.btn)
        # end camera
        
        # Load Image
        self.img_path = 'images/1.jpg'
        self.img = Image(source=self.img_path)
        self.img.allow_stretch = True
        self.img.keep_ratio = True
        self.img.size = (640, 480)
        self.img.pos = (0, 0)
        self.img.opacity = 1

        Parent.add_widget(self.img)

        #self.start_pos = [touch.x, touch.y]
        #print("Start pos:", self.start_pos)

        return Parent
'''    
def show_popup():
    show = P()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400))

    popupWindow.open()
'''
#import CBint
if __name__ == "__main__":
    TouchApp().run()
    
print ("Finished")
