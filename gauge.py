from tkinter import Canvas
from math import sin, cos, radians
from util import generateColors


class Gauge(Canvas):

    def __init__(
        self,
        value=0,
        max_v=250,
        min_v=0,
        max_angle=240,
        size=120,
        partition=4,
        loc={"x": 50, "y": 50},
        col_range=[[255, 0, 0], [0, 0, 255]],
    ):
        super().__init__()
        self.value = value
        self.max_v = max_v
        self.min_v = min_v
        self.max_angle = max_angle
        self.size = size
        self.partition = partition
        self.loc = loc
        self.col_range = col_range
        self.color_set = generateColors(self.col_range, self.partition - 1)
        self.initUI()

    def initUI(self):
        self.configure(width=200, height=200)
        self.drawGauge()

    def setValue(self, value):
        self.value = value
        self.delete("pointer")
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def drawGauge(self):
        TICK_LEN = 10
        TICK_WID = 3
        ARC_WIDTH = 3
        self.create_text(
            self.loc["x"] + self.size / 2,
            self.loc["y"] - 20,
            text="GAUGE",
        )
        self.drawTick(self.min_v, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
        for i in range(self.partition):
            self.drawArc(
                self.loc,
                self.size,
                self.max_angle / self.partition * i - (self.max_angle - 180) / 2,
                self.max_angle / self.partition,
                self.color_set[i],
                ARC_WIDTH,
            )
            self.drawTick(
                self.max_v / self.partition * i, TICK_LEN, TICK_WID, ARC_WIDTH / 2
            )
        self.drawTick(self.max_v, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def drawArc(self, loc, size, start_angle, angle, color, wid):
        self.create_arc(
            loc["x"],
            loc["y"],  # top left
            loc["x"] + size,
            loc["y"] + size,  # bottom right
            start=start_angle,
            extent=angle,  # start angle how far to go
            style="arc",  # draw arc rather than fan
            outline=color,
            width=wid,
        )

    def drawTick(self, value, len, wid, offset):
        x_center = self.loc["x"] + self.size / 2
        y_center = self.loc["y"] + self.size / 2
        theta = 180 - (
            value * self.max_angle / (self.max_v - self.min_v)
            - (self.max_angle - 180) / 2
        )
        up_x, up_y = self.getLocOnArc(x_center, y_center, self.size / 2 + offset, theta)
        down_x, down_y = self.getLocOnArc(
            x_center, y_center, self.size / 2 + offset - len, theta
        )
        self.create_line(up_x, up_y, down_x, down_y, width=wid)

    def drawPointer(self, value):
        PIVOT_SIZE = 5
        PIVOT_COL = "silver"
        POINTER_UP = 0.8
        x_center = self.loc["x"] + self.size / 2
        y_center = self.loc["y"] + self.size / 2
        # draw the pointer
        theta = 180 - (
            value * self.max_angle / (self.max_v - self.min_v)
            - (self.max_angle - 180) / 2
        )
        up_x, up_y = self.getLocOnArc(
            x_center, y_center, self.size * POINTER_UP / 2, theta
        )
        down_x, down_y = self.getLocOnArc(
            x_center, y_center, self.size * (1 - POINTER_UP) / 2, theta + 180
        )
        self.create_line(up_x, up_y, down_x, down_y, width=3, tags="pointer")
        self.drawPivot(x_center, y_center, PIVOT_SIZE, PIVOT_COL)

    def drawPivot(self, x, y, size, color):
        # draw the pivot
        self.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=color,
            outline="",
        )

    def drawDisplay(self, value):
        section = (
            self.partition
            - 1
            - (value - self.min_v) * self.partition // (self.max_v - self.min_v)
        )
        text = self.create_text(
            self.loc["x"] + self.size / 2,
            self.loc["y"] + self.size + 15,
            text=value,
            font=("Helvetica", 10),
            fill="white",
            tags="display",
        )
        bbox = self.bbox(text)
        box = self.create_rectangle(
            bbox, outline="purple", fill=self.color_set[section]
        )
        self.tag_raise(text, box)

    def getLocOnArc(self, center_x, center_y, r, theta):
        theta = radians(theta)
        x = r * cos(theta) + center_x
        y = center_y - r * sin(theta)  # Invert y due to Tkinter's coordinate system
        return x, y
