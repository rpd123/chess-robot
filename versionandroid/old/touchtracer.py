__version__ = '1.0'

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random



class Touchtracer(FloatLayout):

    def on_touch_down(self, touch):
        if not self.img.collide_point(*touch.pos):
            return False
        win = self.get_parent_window()
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        pointsize = 5
        if 'pressure' in touch.profile:
           ud['pressure'] = touch.pressure
           pointsize = (touch.pressure * 100000) ** 2
           ud['color'] = random()

        with self.canvas:
            Color(ud['color'], 1, 1, mode='hsv', group=g)
            ud['lines'] = [
            Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
            Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
            Point(points=(touch.x, touch.y), source='particle.png',
                  pointsize=pointsize, group=g)]

        ud['label'] = Label(size_hint=(None, None))
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        touch.grab(self)
        return True



    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud['label'])

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


class TouchtracerApp(App):


    def build(self):
        return Touchtracer()

    def on_pause(self):
        return True

if __name__ == '__main__':
    TouchtracerApp().run()