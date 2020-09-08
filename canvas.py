from kivy.app import App
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)


class DrawingSpace(StencilView):
    _prev_x = None
    _prev_y = None
    brush_color = (0, 0, 0)
    brush_size = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        if super(DrawingSpace, self).on_touch_move(touch):
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
        if super(DrawingSpace, self).on_touch_up(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        self._prev_x, self._prev_y = None, None
        return True


class IconButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if value == 'down':
            self.color = [1, 0, 0, 1]
        else:
            self.color = [1, 1, 0, 1]


class DrawingApp(App):
    colors = {'Red': (1, 0, 0), 'Blue': (0, 0, 1), 'Green': (0, 1, 0), 'Black': (0, 0, 0)}

    def build(self):
        main_layout = BoxLayout(spacing=10, orientation='vertical')
        controls_layout = BoxLayout(spacing=5, orientation='horizontal', size_hint=(1, .07))
        screen = DrawingSpace(size_hint=(1, 1))

        colors_selector = self.build_color_dropdown(screen)
        size_selector = self.build_size_dropdown(screen)

        controls_layout.add_widget(IconButton(source="res/brush.png", group="tools"))
        controls_layout.add_widget(IconButton(source="res/eraser.png", group="tools"))
        controls_layout.add_widget(colors_selector)
        controls_layout.add_widget(size_selector)

        main_layout.add_widget(controls_layout)
        main_layout.add_widget(screen)

        return main_layout

    def build_size_dropdown(self, screen):
        spinner = Spinner(
            text='5',
            values=tuple([str(i) for i in range(1, 11)]),
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        def show_selected_value(spinner, text):
            screen.brush_size = int(text)

        spinner.bind(text=show_selected_value)
        return spinner

    def build_color_dropdown(self, screen):
        spinner = Spinner(
            text='Black',
            values=tuple([color for color in self.colors]),
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        def show_selected_value(spinner, text):
            screen.brush_color = self.colors[text]

        spinner.bind(text=show_selected_value)
        return spinner


if __name__ == '__main__':
    DrawingApp().run()
