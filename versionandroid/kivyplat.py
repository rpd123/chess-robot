#import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
thetext = "Push Me to switch on steppers and start game"
# class in which we are creating the button

class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        mybutton = Button(
               text =thetext,
               font_size ="20sp",
               background_color =(2, 1, 1, 1),
               color =(1, 1, 1, 1),
               size =(480, 32),
               size_hint =(None, None),
               #pos_hint ={None, None},
               pos =(150,150)
                          )
        mybutton.bind(on_press = self.say_hello) # Note: here say_hello doesn't have brackets.
        self.add_widget(mybutton)

    def say_hello(self, mybutton):
        self.remove_widget(mybutton)
        print ("hello")

class BtnApp(App):
    def build(self):
        return Launch()
    print("Finnished")    
BtnApp().run()
thetext="moo"
BtnApp().run()
print("Finished")