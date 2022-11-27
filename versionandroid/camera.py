# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)
import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '780')
import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    spacing: 0
''')

mydir = "images/"
class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        
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
        self.add_widget(self.camera)
        self.add_widget(self.btn)
         
    def capture(self, btn):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png(mydir+"5.png")
        print("Captured")
        

        img = cv2.imread(mydir+'5.png')
        cv2.imwrite(mydir+'5.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        
        #self.remove_widget(self.camera)
        #self.remove_widget(btn)

class MyCamera(App):

    def build(self):
        return CameraClick()

MyCamera().run()
