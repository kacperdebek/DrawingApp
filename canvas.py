from kivy.app import App
from kivy.graphics import *
from kivy.uix.widget import Widget


class Screen(Widget):
    _prev_x = None
    _prev_y = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update()

    def on_touch_move(self, touch):
        if super(Screen, self).on_touch_move(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        if self._prev_x and self._prev_y:
            with self.canvas:
                Color(1., 0, 0)
                Line(points=[self._prev_x, self._prev_y, touch.x, touch.y], width=10)
        self._prev_x, self._prev_y = touch.x, touch.y
        return True

    def on_touch_up(self, touch):
        if super(Screen, self).on_touch_up(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        self._prev_x, self._prev_y = None, None
        return True


class TestApp(App):
    def build(self):
        return Screen()


TestApp().run()
