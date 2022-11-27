# import kivy module    
import kivy  
       
# base Class of your App inherits from the App class.    
# app:always refers to the instance of your application   
from kivy.app import App 
     
# this restrict the kivy version i.e  
# below this kivy version you cannot  
# use the app or software  
kivy.require('1.9.0') 
    
# The Label widget is for rendering text.  
from kivy.uix.label import Label 
    
# module consist the floatlayout  
# to work with FloatLayout first  
# you have to import it  
from kivy.uix.floatlayout import FloatLayout 
  
# Scatter is used to build interactive
# widgets that can be translated,
# rotated and scaled with two or more
# fingers on a multitouch system.
from kivy.uix.scatter import Scatter
  
# The TextInput widget provides a
# box for editable plain text
from kivy.uix.textinput import TextInput

from kivy.core.window import Window
from kivy.lang import Builder
# Create the App class
class TestApp(App):
    def carryon(self):        
        print ("boo")
    
    def on_enter(instance, value):
        print('The widget', instance, 'have:', value)
        #print(textinput.text)
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
  
      
          
        return True
  
# Run the App
if __name__ == "__main__":
    TestApp().run()