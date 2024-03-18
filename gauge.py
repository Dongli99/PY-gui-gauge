from tkinter import Canvas
from math import sin, cos, radians
from util import generateColors


class Gauge(Canvas):

    MAX_VALUE = 250
    MIN_VALUE = 0
    MAX_ANGLE = 270
    SIZE = 120
    PARTITION = 4
    START_LOC = {"x": 50, "y": 20}
    COLORS_RANGE = [[255, 0, 0], [0, 0, 255]]  # red and blue

    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.initUI()

    def initUI(self):
        self.configure(width=200, height=200)
        self.drawGauge()

    def setValue(self, value):
        self.value = value
        self.delete("pointer")
        self.drawPointer(self.value)

    def drawGauge(self):
        TICK_LEN = 10
        TICK_WID = 3
        ARC_WIDTH = 3
        self.drawTick(Gauge.MIN_VALUE, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
        for i in range(Gauge.PARTITION):
            self.drawArc(
                Gauge.START_LOC,
                Gauge.SIZE,
                Gauge.MAX_ANGLE / Gauge.PARTITION * i - (Gauge.MAX_ANGLE - 180) / 2,
                Gauge.MAX_ANGLE / Gauge.PARTITION,
                generateColors(Gauge.COLORS_RANGE, Gauge.PARTITION - 1)[i],
                ARC_WIDTH,
            )
            self.drawTick(
                Gauge.MAX_VALUE / Gauge.PARTITION * i, TICK_LEN, TICK_WID, ARC_WIDTH / 2
            )
        self.drawTick(Gauge.MAX_VALUE, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
        self.drawPointer(self.value)

    def drawArc(self, start_loc, size, start_angle, angle, color, wid):
        self.create_arc(
            start_loc["x"],
            start_loc["y"],  # top left
            start_loc["x"] + size,
            start_loc["y"] + size,  # bottom right
            start=start_angle,
            extent=angle,  # start angle how far to go
            style="arc",  # draw arc rather than fan
            outline=color,
            width=wid,
        )

    def drawTick(self, value, len, wid, offset):
        x_center = Gauge.START_LOC["x"] + Gauge.SIZE / 2
        y_center = Gauge.START_LOC["y"] + Gauge.SIZE / 2
        theta = 180 - (
            value * Gauge.MAX_ANGLE / (Gauge.MAX_VALUE - Gauge.MIN_VALUE)
            - (Gauge.MAX_ANGLE - 180) / 2
        )
        up_x, up_y = self.getLocOnArc(
            x_center, y_center, Gauge.SIZE / 2 + offset, theta
        )
        down_x, down_y = self.getLocOnArc(
            x_center, y_center, Gauge.SIZE / 2 + offset - len, theta
        )
        self.create_line(up_x, up_y, down_x, down_y, width=wid)

    def drawPointer(self, value):
        PIVOT_SIZE = 5
        PIVOT_COL = "silver"
        POINTER_UP = 0.8
        x_center = Gauge.START_LOC["x"] + Gauge.SIZE / 2
        y_center = Gauge.START_LOC["y"] + Gauge.SIZE / 2
        self.drawPivot(x_center, y_center, PIVOT_SIZE, PIVOT_COL)
        # draw the pointer
        theta = 180 - (
            value * Gauge.MAX_ANGLE / (Gauge.MAX_VALUE - Gauge.MIN_VALUE)
            - (Gauge.MAX_ANGLE - 180) / 2
        )
        up_x, up_y = self.getLocOnArc(
            x_center, y_center, Gauge.SIZE * POINTER_UP / 2, theta
        )
        down_x, down_y = self.getLocOnArc(
            x_center, y_center, Gauge.SIZE * (1 - POINTER_UP) / 2, theta + 180
        )
        self.create_line(up_x, up_y, down_x, down_y, width=3, tags="pointer")

    def drawPivot(self, x_center, y_center, size, color):
        # draw the pivot
        self.create_oval(
            x_center - size,
            y_center - size,
            x_center + size,
            y_center + size,
            fill=color,
            outline="",
        )

    def getLocOnArc(self, center_x, center_y, r, theta):
        theta = radians(theta)
        x = r * cos(theta) + center_x
        y = center_y - r * sin(theta)  # Invert y due to Tkinter's coordinate system
        return x, y
