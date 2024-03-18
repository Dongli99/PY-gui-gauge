from VoiceDataGenerator import VoiceDataGenerator
from tkinter import Tk, Canvas, Frame, BOTH, W
from math import sin, cos, radians


class DataDisplay(Tk):
    pass


class Gauge(Canvas):

    MAX_VALUE = 250
    MIN_VALUE = 0
    MAX_ANGLE = 270
    SIZE = 120
    PARTITION = 4
    START_LOC = {"x": 50, "y": 100}
    COLORS_RANGE = [[255, 0, 0], [0, 0, 255]]  # red and blue

    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.initUI()

    def initUI(self):
        self.configure(width=200, height=200)
        self.drawGauge()

    def drawGauge(self):
        for i in range(Gauge.PARTITION):
            self.drawArc(
                Gauge.START_LOC,
                Gauge.SIZE,
                Gauge.MAX_ANGLE / Gauge.PARTITION * i - (Gauge.MAX_ANGLE - 180) / 2,
                Gauge.MAX_ANGLE / Gauge.PARTITION,
                self.generate_colors(Gauge.COLORS_RANGE, Gauge.PARTITION - 1)[i],
            )
        self.drawPointer(180)

    def drawArc(self, start_loc, size, start_angle, angle, color):
        self.create_arc(
            start_loc["x"],
            start_loc["y"],  # top left
            start_loc["x"] + size,
            start_loc["y"] + size,  # bottom right
            start=start_angle,
            extent=angle,  # start angle how far to go
            style="arc",  # draw arc rather than fan
            outline=color,
            width=5,
        )

    def drawTick(self, size, angle):
        pass

    def drawPointer(self, value):
        def get_loc_on_arc(center_x, center_y, r, theta):
            theta = radians(theta)
            x = r * cos(theta) + center_x
            y = center_y - r * sin(theta)  # Invert y due to Tkinter's coordinate system
            return x, y

        PIVOT_SIZE = 5
        PERCENT_UP = 0.8
        x_center = Gauge.START_LOC["x"] + Gauge.SIZE / 2
        y_center = Gauge.START_LOC["y"] + Gauge.SIZE / 2
        # draw the pivot
        self.create_oval(
            x_center - PIVOT_SIZE,
            y_center - PIVOT_SIZE,
            x_center + PIVOT_SIZE,
            y_center + PIVOT_SIZE,
            fill="silver",
            outline="",
        )
        # draw the pointer
        theta = 180 - (
            value * Gauge.MAX_ANGLE / Gauge.MAX_VALUE - (Gauge.MAX_ANGLE - 180) / 2
        )
        up_x, up_y = get_loc_on_arc(
            x_center, y_center, Gauge.SIZE * PERCENT_UP / 2, theta
        )
        down_x, down_y = get_loc_on_arc(
            x_center, y_center, Gauge.SIZE * (1 - PERCENT_UP) / 2, theta + 180
        )
        self.create_line(up_x, up_y, down_x, down_y)

    def set_value(self, value):
        pass

    def generate_colors(self, c_range, steps):
        def hex_color(rgb):
            red = int(rgb[0])
            green = int(rgb[1])
            blue = int(rgb[2])
            return "#{:02x}{:02x}{:02x}".format(red, green, blue)

        colors = []
        colors.append(hex_color(c_range[0]))
        red = c_range[0][0]
        green = c_range[0][1]
        blue = c_range[0][2]
        for i in range(steps):
            red += (c_range[-1][0] - c_range[0][0]) / steps
            green += (c_range[-1][1] - c_range[0][1]) / steps
            blue += (c_range[-1][2] - c_range[0][2]) / steps
            colors.append(hex_color([red, green, blue]))
        colors.append(hex_color(c_range[-1]))
        return colors


def main():
    root = Tk()
    gauge = Gauge()
    gauge.pack(fill=BOTH, expand=1)
    root.mainloop()


if __name__ == "__main__":
    main()
