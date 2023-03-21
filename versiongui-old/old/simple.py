from kivy.app import App
from kivy.uix.widget import Widget

class test( Widget ):

    def __init__(self, **kwargs):
        super (test, self).__init__(**kwargs)
        
        self.pos = (0,0)
        self.size = (100,100)

    def on_touch_down( self, touch ):

        if self.collide_point( *touch.pos ):
            print ("inside")
        else:
            print ("outside")
class simple(App):
    def build(self):
        return test()

if __name__ == "__main__":
    simple().run()