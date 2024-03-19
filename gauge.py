import random
from tkinter import *
from tkinter import messagebox
from math import sin, cos, radians
from util import generateColors, generateRandomColor


class Gauge(Frame):

    def __init__(
        self,
        value=0,
        max_v=250,
        min_v=0,
        max_angle=240,
        size=320,
        partition=4,
        loc=(50, 80),
        col_range=[[255, 215, 0], [32, 178, 170]],
    ):
        super().__init__()
        self.value = value
        self.value_var = IntVar()
        self.max_v = max_v
        self.min_v = min_v
        self.max_angle = max_angle
        self.size = size
        self.partition = partition
        self.loc = loc
        self.col_range = col_range
        self.initUI()

    def setValue(self, value):
        self.value = value
        self.canvas.delete("pointer")
        self.canvas.delete("display_box")
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def initUI(self):
        self.master.title("Lab 9 A & B")
        self.pack(fill=BOTH, expand=1)
        self.drawTop()
        self.drawBottom()

    def drawArc(self, loc, size, start_angle, angle, color, wid):
        self.canvas.create_arc(
            loc[0],
            loc[1],  # top left
            loc[0] + size,
            loc[1] + size,  # bottom right
            start=start_angle,
            extent=angle,  # start angle how far to go
            style="arc",  # draw arc rather than fan
            outline=color,
            width=wid,
            tags="arc",
        )

    def drawTick(self, value, len, wid, offset):
        x_center = self.loc[0] + self.size / 2
        y_center = self.loc[1] + self.size / 2
        theta = 180 - (
            value * self.max_angle / (self.max_v - self.min_v)
            - (self.max_angle - 180) / 2
        )
        up_x, up_y = self.getLocOnArc(x_center, y_center, self.size / 2 + offset, theta)
        down_x, down_y = self.getLocOnArc(
            x_center, y_center, self.size / 2 + offset - len, theta
        )
        self.canvas.create_line(up_x, up_y, down_x, down_y, width=wid)
        tag_x, tag_y = self.getLocOnArc(
            x_center, y_center, self.size / 2 + offset - len - 15, theta
        )
        self.canvas.create_text(
            tag_x, tag_y, text=round(value), font=("Helvetica", 12, "italic")
        )

    def drawPointer(self, value):
        PIVOT_SIZE = 5
        PIVOT_COL = "silver"
        POINTER_UP = 0.8
        x_center = self.loc[0] + self.size / 2
        y_center = self.loc[1] + self.size / 2
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
        self.canvas.create_line(up_x, up_y, down_x, down_y, width=4, tags="pointer")
        self.drawPivot(x_center, y_center, PIVOT_SIZE, PIVOT_COL)

    def drawPivot(self, x, y, size, color):
        # draw the pivot
        self.canvas.create_oval(
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
        text = self.canvas.create_text(
            self.loc[0] + self.size / 2,
            self.loc[1] + self.size + 15,
            text=value,
            font=("Helvetica", 20),
            fill="white",
            tags="display",
        )
        bbox = self.canvas.bbox(text)
        box = self.canvas.create_rectangle(
            bbox, outline="", fill=self.color_set[section], tags="display_box"
        )
        self.canvas.tag_raise(text, box)

    def drawTop(self):
        frame = Frame(self)
        frame.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.75)
        self.canvas = Canvas(frame)
        self.canvas.pack(fill=BOTH, expand=1)
        self.tick_wid = 3
        self.arc_wid = 10
        self.color_set = generateColors(self.col_range, self.partition - 1)
        self.canvas.create_text(
            self.loc[0] + self.size / 2,
            self.loc[1] - 30,
            text="GAUGE",
            font=("Helvetica", 12, "bold"),
        )
        self.drawTick(self.min_v, self.arc_wid * 2, self.tick_wid, self.arc_wid / 2)
        for i in range(self.partition):
            self.drawArc(
                self.loc,
                self.size,
                self.max_angle / self.partition * i - (self.max_angle - 180) / 2,
                self.max_angle / self.partition,
                self.color_set[i],
                self.arc_wid,
            )
            self.drawTick(
                self.max_v / self.partition * i,
                self.arc_wid * 2,
                self.tick_wid,
                self.arc_wid / 2,
            )
        self.drawTick(self.max_v, self.arc_wid * 2, self.tick_wid, self.arc_wid / 2)
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def drawBottom(self):
        def handleUpdate():
            value = int(self.value_var.get())
            if value <= self.max_v and value >= self.min_v:
                self.setValue(value)
            else:
                messagebox.showinfo(
                    "Invalid Value",
                    f"Value must be between {self.min_v} - {self.max_v}",
                )

        def handleLucky():
            self.col_range[0] = generateRandomColor()
            self.col_range[1] = generateRandomColor()
            self.color_set = generateColors(self.col_range, self.partition - 1)
            self.max_angle = random.randint(90, 330)
            self.partition = random.randint(3, 10)
            self.canvas.delete("arc")
            self.drawTop()
            self.setValue(random.randint(0, 250))

        frame = Frame(self)
        frame.place(relx=0.03, rely=0.8, relwidth=0.94, relheight=0.1)
        entry = Entry(frame, textvariable=self.value_var)
        entry.place(relx=0.47, rely=0.35, relwidth=0.06, relheight=0.4)
        submit_btn = Button(frame, text="UPDATE", command=handleUpdate)
        submit_btn.place(relx=0.56, rely=0.35, relwidth=0.12, relheight=0.4)
        lucky_btn = Button(frame, text="LUCKY", command=handleLucky)
        lucky_btn.place(relx=0.32, rely=0.35, relwidth=0.12, relheight=0.4)

    def getLocOnArc(self, center_x, center_y, r, theta):
        theta = radians(theta)
        x = r * cos(theta) + center_x
        y = center_y - r * sin(theta)  # Invert y due to Tkinter's coordinate system
        return x, y


if __name__ == "__main__":
    root = Tk()
    root.geometry("440x600+300+300")
    gauge = Gauge()
    root.mainloop()
