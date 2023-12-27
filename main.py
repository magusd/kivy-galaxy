from kivy.app import App
from kivy.config import Config
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget

Config.set('graphics', 'width', 1350)
Config.set('graphics', 'height', 600)


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    FPS = 60

    current_offset_y = 0
    SPEED = 8

    current_offset_x = 0
    SPEED_X = 12

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
        Clock.schedule_interval(self.update, 1.0 / self.FPS)

    def on_parent(self, widget, parent):
        pass
        # print(f"parent: width {self.width} height {self.height}")

    def on_size(self, *args):
        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75

    def on_perspective_point_x(self, widget, value):
        pass
        # print(f"perspective_point_x {value}")

    def on_perspective_point_y(self, widget, value):
        pass
        # print(f"perspective_point_y {value}")

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

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y  # 1 when at the bottom, 0 at the top
        factor_y = pow(factor_y, 2)

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(tr_x), int(tr_y)

    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            self.curret_speed_x = self.SPEED_X
        else:
            self.curret_speed_x = -self.SPEED_X

    def on_touch_up(self, touch):
        self.curret_speed_x = 0

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
