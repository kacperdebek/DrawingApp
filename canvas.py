from kivy.app import App
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)


class Screen(Widget):
    _prev_x = None
    _prev_y = None
    brush_color = (0, 0, 0)
    brush_size = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        if super(Screen, self).on_touch_move(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        if self._prev_x and self._prev_y:
            with self.canvas:
                Color(self.brush_color[0], self.brush_color[1], self.brush_color[2])
                Line(points=[self._prev_x, self._prev_y, touch.x, touch.y], width=self.brush_size)
        self._prev_x, self._prev_y = touch.x, touch.y
        return True

    def on_touch_up(self, touch):
        if super(Screen, self).on_touch_up(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        self._prev_x, self._prev_y = None, None
        return True


class IconButton(ButtonBehavior, Image):
    pass


class DrawingApp(App):
    colors = {'Red': (1, 0, 0), "Blue": (0, 0, 1), "Green": (0, 1, 0)}

    def build(self):
        main_layout = BoxLayout(spacing=10, orientation='vertical')
        controls_layout = BoxLayout(spacing=1, orientation='horizontal', size_hint=(1, .07))
        screen = Screen(size_hint=(1, 1))

        dropdown = DropDown()
        for color, rgb in self.colors.items():
            rgb = list(rgb) + [1]
            btn = Button(text=color, color=rgb, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        main_button = IconButton(source="res/color_wheel.png")
        main_button.bind(on_release=dropdown.open)

        dropdown.bind(on_select=lambda instance, x: setattr(screen, 'brush_color', self.colors.get(x)))

        controls_layout.add_widget(main_button)

        main_layout.add_widget(controls_layout)
        main_layout.add_widget(screen)

        return main_layout


if __name__ == '__main__':
    DrawingApp().run()
