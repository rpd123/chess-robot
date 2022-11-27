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
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from kivy.uix.popup import Popup
#mytext ="ooh"
class P(FloatLayout):
    '''
    def __init__(self, **kwargs):
        super(P, self).__init__(**kwargs)
        mybutton = Button(
               text =mytext,
               font_size ="20sp",
               background_color =(2, 1, 1, 1),
               color =(1, 1, 1, 1),
               size =(150, 22),
               size_hint =(None, None),
               #pos_hint ={None, None},
               pos =(150,150)
               #on_press= self.btnpressed()
               )    
        #self.add_widget(mybutton)
    '''
class TouchInput(Widget):
    def __init__(self, **kwargs):
        super(TouchInput, self).__init__(**kwargs)
        self.start_pos = [0, 0]
        self.end_pos = [0, 0]
        self.img_path = 'images/1.jpg'
        
    def but_press(self):
        print("But is pressed!")
    '''
    def on_touch_down(self, touch):
        with self.canvas:
            self.canvas.clear()
            # Load Image
            self.img = Image(source=self.img_path)
            self.img.allow_stretch = True
            self.img.keep_ratio = True
            self.img.size = self.size

            # Position set
            self.img.pos = (0, 0)
            self.img.opacity = 1


            self.start_pos = [touch.x, touch.y]
            print("Start pos:", self.start_pos)
    '''

             
    def dispop(self, mytext):
    #def show_popup():
        #mytext = mmtext
        print (mytext)
        show = P()

        self.popup = Popup(title=mytext, content=show, size_hint=(None,None),size=(150, 22), auto_dismiss=True)
        
        #popupWindow.open()
        # create content and add to the popup
        #content = Button(text=mytext, size=(250,32), size_hint =(None, None), pos =(200,150))
        #popup = Popup(content=content, auto_dismiss=False)
        #popup.open()
        
        #bind the on_press event of the button to the dismiss function
        self.popup.bind(on_press=self.popup.dismiss)

        # open the popup
        self.popup.open()
        #time.sleep(1)
        #popup.dismiss()
        
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
            self.dispop(mytext)
            '''
            if self.start_pos == self.end_pos:
                print("Same position")

            elif (self.start_pos[0] < self.end_pos[0]) and (self.start_pos[1] < self.end_pos[1]):
                print("Top Right")
                rect_start_point = self.start_pos
                rect_size = [abs(self.start_pos[0] - self.end_pos[0]), abs(self.start_pos[1] - self.end_pos[1])]

                print("Pos:", self.start_pos, "Size:", rect_size)
                self.dispop("Pos: ")
                Color(rgba=(100 / 255, 143 / 255, 165 / 255, 0.6))
                self.rect = Rectangle(pos=rect_start_point, size=(rect_size))

            elif (self.start_pos[0] < self.end_pos[0]) and (self.start_pos[1] > self.end_pos[1]):
                print("Bottom Right")
                rect_start_point = [self.start_pos[0], self.end_pos[1]]
                rect_size = [abs(self.start_pos[0] - self.end_pos[0]), abs(self.start_pos[1] - self.end_pos[1])]

                print("Pos:", self.start_pos, "Size:", rect_size)
                Color(rgba=(23 / 255, 143 / 255, 54 / 255, 0.6))
                self.rect = Rectangle(pos=rect_start_point, size=(rect_size))

            elif (self.start_pos[0] > self.end_pos[0]) and (self.start_pos[1] < self.end_pos[1]):
                print("Top Left")
                rect_start_point = [self.end_pos[0], self.start_pos[1]]
                rect_size = [abs(self.start_pos[0] - self.end_pos[0]), abs(self.start_pos[1] - self.end_pos[1])]

                print("Pos:", self.start_pos, "Size:", rect_size)
                Color(rgba=(100 / 255, 93 / 255, 65 / 255, 0.6))
                self.rect = Rectangle(pos=rect_start_point, size=(rect_size))

            elif (self.start_pos[0] > self.end_pos[0]) and (self.start_pos[1] > self.end_pos[1]):
                print("Bottom Left")
                rect_start_point = self.end_pos
                rect_size = [abs(self.start_pos[0]-self.end_pos[0]), abs(self.start_pos[1]-self.end_pos[1])]

                print("Pos:", self.start_pos, "Size:", rect_size)
                Color(rgba=(100 / 255, 45 / 255, 34 / 255, 0.6))
                self.rect = Rectangle(pos=rect_start_point, size=(rect_size))

            else:
                print("Same Axis")
            '''
class TouchApp(App):
    
    def clear_canvas(self,obj):
        self.ROI.canvas.clear()

    def build(self):
        Parent = BoxLayout()
        self.ROI = TouchInput()
        Parent.add_widget(self.ROI)
        #but = Button(text="clear", size_hint_x=0.2)
        #but.bind(on_release=self.clear_canvas)
        #Parent.add_widget(but)
        #self.load_kv("overlay.kv")
        
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
    
def show_popup():
    show = P()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400))

    popupWindow.open()
    
if __name__ == "__main__":
    TouchApp().run()
