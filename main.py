from kivy import platform
from kivy.config import Config
from kivy.metrics import dp

Config.set('graphics', 'width', 1350)
Config.set('graphics', 'height', 600)

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from transforms import transform, transform_perspective, transform_2D
    from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    FPS = 60

    current_offset_y = 0
    SPEED = 8

    current_offset_x = 0
    SPEED_X = dp(20)

    V_NB_LINES = 15
    V_LINES_SPACING = .2
    vertical_lines = []

    H_NB_LINES = 8
    H_LINES_SPACING = .2
    horizontal_lines = []
    curret_speed_x = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / self.FPS)

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.V_NB_LINES):
                self.vertical_lines.append(Line(points=[], width=2))

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.H_NB_LINES):
                self.horizontal_lines.append(Line(points=[], width=2))

    def is_desktop(self):
        if platform in ('linux', 'macosx', 'windows'):
            return True
        else:
            return False

    # Vitor
    # def update_vertical_lines(self):
    #     with self.canvas:
    #         spacing = self.V_LINES_SPACING * self.width
    #         x_inc = int(self.width / (self.V_NB_LINES + 1))
    #         for i, vertical_line in enumerate(self.vertical_lines):
    #             print(i)
    #             x = x_inc * (i + 1)
    #             vertical_line.points = [x, 0, x, self.height]

    def update_vertical_lines(self):
        central_line_x = int(self.width / 2) + self.current_offset_x
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset * spacing)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def update_horizontal_lines(self):
        x_min = self.vertical_lines[0].points[0]
        x_max = self.vertical_lines[-1].points[0]
        for i in range(0, self.H_NB_LINES):
            line_y = i * self.H_LINES_SPACING * self.height - self.current_offset_y

            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        time_factor = dt * self.FPS
        self.current_offset_y += self.SPEED * time_factor

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y > spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.curret_speed_x * time_factor

        self.update_vertical_lines()
        self.update_horizontal_lines()


class GalaxyApp(App):
    pass


if __name__ == '__main__':
    GalaxyApp().run()
