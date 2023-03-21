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
               #on_press= self.btnpressed()
               )
        #mybutton.unbind(on_press = self.say_hello)
        mybutton.bind(on_press = self.say_hello) # Note: here say_hello doesn't have brackets.
        #mybutton.bind(on_request_close=self.end_func)
        self.add_widget(mybutton)

    def say_hello(self, mybutton):
        #self.remove_widget(mybutton)
        mybutton.set_opacity = 0.40
        #self.clear_widgets()
        print ("hello")
        
        BtnApp.get_running_app().stop()
        #BtnApp().stop()

class BtnApp(App):
    def build(self):
        return Launch()
    print("Finnished")

BtnApp().run()
print("Not Finished")
thetext="moo"
#BtnApp().run()
print("Finished")