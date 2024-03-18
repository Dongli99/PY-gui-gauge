from tkinter import Canvas
from math import sin, cos, radians
from util import generateColors


class Gauge(Canvas):

    MAX_VALUE = 250
    MIN_VALUE = 0
    MAX_ANGLE = 270
    SIZE = 120
    PARTITION = 4
    LOCATION = {"x": 50, "y": 50}
    COLORS_RANGE = [[255, 0, 0], [0, 0, 255]]  # red and blue

    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.color_set = generateColors(Gauge.COLORS_RANGE, Gauge.PARTITION - 1)
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
            Gauge.LOCATION["x"] + Gauge.SIZE / 2,
            Gauge.LOCATION["y"] - 20,
            text="GAUGE",
        )
        self.drawTick(Gauge.MIN_VALUE, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
        for i in range(Gauge.PARTITION):
            self.drawArc(
                Gauge.LOCATION,
                Gauge.SIZE,
                Gauge.MAX_ANGLE / Gauge.PARTITION * i - (Gauge.MAX_ANGLE - 180) / 2,
                Gauge.MAX_ANGLE / Gauge.PARTITION,
                self.color_set[i],
                ARC_WIDTH,
            )
            self.drawTick(
                Gauge.MAX_VALUE / Gauge.PARTITION * i, TICK_LEN, TICK_WID, ARC_WIDTH / 2
            )
        self.drawTick(Gauge.MAX_VALUE, TICK_LEN, TICK_WID, ARC_WIDTH / 2)
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
        x_center = Gauge.LOCATION["x"] + Gauge.SIZE / 2
        y_center = Gauge.LOCATION["y"] + Gauge.SIZE / 2
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
        x_center = Gauge.LOCATION["x"] + Gauge.SIZE / 2
        y_center = Gauge.LOCATION["y"] + Gauge.SIZE / 2
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
            Gauge.PARTITION
            - 1
            - (value - Gauge.MIN_VALUE)
            * Gauge.PARTITION
            // (Gauge.MAX_VALUE - Gauge.MIN_VALUE)
        )
        text = self.create_text(
            Gauge.LOCATION["x"] + Gauge.SIZE / 2,
            Gauge.LOCATION["y"] + Gauge.SIZE + 15,
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
