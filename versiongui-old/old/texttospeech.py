import kivy
kivy.require('1.7.1')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.popup import Popup

from plyer import tts

__version__ = '1.1.12'


class SayThis(BoxLayout):
    saywhat_text = ObjectProperty(None)
    
    def say_something(self, text):
        try:
            tts.speak(text)
        except NotImplementedError:
            popup = Popup(title='TTS Not Implemented',
                          content=Label(text='Sorry. TTS is not available.'),
                          size_hint=(None, None), 
                          size=(300, 300))
            popup.open()
    
    def clear(self):
        self.saywhat_text.text = ""
        self.saywhat_text.focus = True


class SayThisApp(App):
    def build(self):
        return SayThis()

    def on_pause(self):
        return True

    def on_resume(self):
        pass 


if __name__ == '__main__':
    SayThisApp().run()