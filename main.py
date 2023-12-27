from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 4
    V_LINES_SPACING = .1
    vertical_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        # print(f"width {self.width} height {self.height}")

    def on_parent(self, widget, parent):
        pass
        # print(f"parent: width {self.width} height {self.height}")

    def on_size(self, *args):
        # center_x = self.width / 2
        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75

        self.update_vertical_lines()
        # print(f"onsize: width {self.width} height {self.height}")
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.width / 0.75

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
        with self.canvas:
            central_line_x = int(self.width / 2)
            spacing = self.V_LINES_SPACING * self.width
            offset = -int(self.V_NB_LINES / 2)
            for i in range(0, self.V_NB_LINES):
                line_x = int(central_line_x + offset * spacing)

                x1, y1 = self.transform(line_x, 0)
                x2, y2 = self.transform(line_x, self.height)

                self.vertical_lines[i].points = [x1, y1, x2, y2]
                offset += 1

    def transform(self, x, y):
        return self.transform_2D(x, y)
        # return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        tr_y = y * self.perspective_point_y / self.height
        if tr_y > self.perspective_point_y:
            tr_y -= self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - tr_y
        proportion = diff_y / self.perspective_point_y  # 1 when at the bottom, 0 at the top
        tr_x = self.perspective_point_x + diff_x * proportion
        return int(tr_x), int(tr_y)


class GalaxyApp(App):
    pass


if __name__ == '__main__':
    GalaxyApp().run()
