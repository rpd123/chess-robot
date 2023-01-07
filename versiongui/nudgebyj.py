import CBstate
import bluetrpd
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TouchApp(App):
    currentangle = 40
    sp, send_stream = bluetrpd.get_socket_stream(CBstate.bluetoothdevicename) 
    def nudgeup(self, plusbutton):
        self.currentangle = self.currentangle + 3
        mycode = "M5 T" + str(self.currentangle) + "\r"
        #print (self.currentangle)
        self.send_stream.write(mycode.encode())        
    
    def nudgedown(self, minusbutton):
        self.currentangle = self.currentangle - 3
        mycode = "M3 T" + str(self.currentangle) + "\r"
        #print (self.currentangle)
        self.send_stream.write(mycode.encode()) 

    def build(self):
        Parent = BoxLayout(orientation='vertical',
                   #minimum_height = '8000dp'
                           )
        self.plusbtn = Button(
            text = 'Nudge up',
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.nudgeup
            )
        Parent.add_widget(self.plusbtn)
        
        self.minusbtn = Button(
            text = 'Nudge down',
            size_hint = (None, None),
            width = CBstate.windowsize[0],
            height = '34dp',
            on_press = self.nudgedown
            )
        Parent.add_widget(self.minusbtn)
        
        return Parent
    
if __name__ == "__main__":
    TouchApp().run()

