from kivy.app import App
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.button import Button
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
            self._prev_x, self._prev_y = None, None
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
    def __init__(self, screen, colors_selector=None, size_selector=None, **kwargs):
        self.screen = screen
        self.colors_selector = colors_selector
        self.size_selector = size_selector
        super(IconButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        for tool in self.get_widgets('tools'):
            if tool.id == widget.id:
                if value == 'down' and tool.id == 'brush':
                    self.color = [0.345, 0.345, 0.345, 1]
                    self.screen.brush_color = DrawingApp.colors[self.colors_selector.text]
                elif value == 'down' and tool.id == 'eraser':
                    self.color = [0.345, 0.345, 0.345, 1]
                    self.screen.brush_color = (1, 1, 1)
                else:
                    self.color = [1, 1, 1, 1]


class DrawingApp(App):
    colors = {'Red': (1, 0, 0), 'Blue': (0, 0, 1), 'Green': (0, 1, 0), 'Black': (0, 0, 0), 'Yellow': (1, 1, 0),
              'Magenta': (1, 0, 1), 'Cyan': (0, 1, 1)}

    def build(self):
        main_layout = BoxLayout(spacing=10, orientation='vertical')
        controls_layout = BoxLayout(spacing=1, orientation='horizontal', size_hint=(1, .07))
        screen = DrawingSpace(size_hint=(1, 1))

        def set_brush_color(spinner, text):
            if screen.brush_color != (1, 1, 1):
                screen.brush_color = self.colors[text]

        def set_brush_size(spinner, text):
            screen.brush_size = int(text.split(' ')[1])

        colors_selector = self.build_spinner(
            "Black",
            tuple([color for color in self.colors]),
            set_brush_color
        )

        size_selector = self.build_spinner(
            "Size: 5",
            tuple(["Size: " + str(i) for i in range(1, 21)]),
            set_brush_size)

        controls_layout.add_widget(
            IconButton(
                pos_hint={'center_x': .45, 'center_y': .45}, id="brush", source="res/brush.png", group="tools",
                state="down", allow_no_selection=False,
                screen=screen, colors_selector=colors_selector, size_selector=size_selector), )
        controls_layout.add_widget(
            IconButton(
                pos_hint={'center_x': .45, 'center_y': .45}, id="eraser", source="res/eraser.png", group="tools",
                allow_no_selection=False, screen=screen,
                colors_selector=colors_selector,
                size_selector=size_selector))

        clear_button = Button(text="Clear",
                              pos_hint={'center_x': .5, 'center_y': .5})
        clear_button.bind(on_press=lambda x: screen.canvas.clear())

        controls_layout.add_widget(clear_button)
        controls_layout.add_widget(colors_selector)
        controls_layout.add_widget(size_selector)

        main_layout.add_widget(controls_layout)
        main_layout.add_widget(screen)

        return main_layout

    def build_spinner(self, initial_text, values_list, func):
        spinner = Spinner(
            text=initial_text,
            values=values_list,
            pos_hint={'center_x': .5, 'center_y': .5})

        spinner.bind(text=func)
        return spinner


if __name__ == '__main__':
    DrawingApp().run()
