from VoiceDataGenerator import VoiceDataGenerator
from tkinter import Tk, Canvas, Frame, BOTH, W


class DataDisplay(Tk):
    pass


class Gauge(Canvas):

    MAX_VALUE = 250
    MIN_VALUE = 0
    MAX_ANGLE = 270
    SIZE = 120
    PARTITION = 4
    START_LOC = {"x": 50, "y": 100}
    COLORS_RANGE = [(255, 0, 0), (0, 0, 255)]  # red and blue

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
                generate_colors(Gauge.COLORS_RANGE, Gauge.PARTITION)[i],
            )

        def generate_colors(self, color_range, number):
            pass

    def drawArc(self, start_loc, size, start_angle, angle, color):
        self.create_arc(
            start_loc["x"],
            start_loc["y"],  # top left
            start_loc["x"] + size,
            start_loc["y"] + size,  # bottom right
            start=start_angle,
            extent=angle,  # start angle how far to go
            style="arc",  # draw arc rather than fan
            outline="#f11",
            width=5,
        )

    def drawTick(self, size, angle):
        pass

    def drawPointer(self, value):
        pass

    def set_value(self, value):
        pass


def main():
    root = Tk()
    gauge = Gauge()
    gauge.pack(fill=BOTH, expand=1)
    root.mainloop()


if __name__ == "__main__":
    main()
