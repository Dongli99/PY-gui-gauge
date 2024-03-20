import random
from tkinter import *
from tkinter import messagebox
from math import sin, cos, radians


class Gauge(Frame):
    """
    Gauge class for creating a customizable gauge widget.

    Attributes:
        value (int): The current value of the gauge.
        max_v (int): The maximum value of the gauge.
        min_v (int): The minimum value of the gauge.
        max_angle (int): The maximum angle (in degrees) of the gauge.
        size (int): The size of the gauge.
        partition (int): The number of partitions in the gauge.
        loc (tuple): The position of the gauge.
        col_range (list): The range of colors for the gauge.
    """

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
        """
        Initialize the Gauge instance with default values or specified parameters.

        Args:
            value (int): The current value of the gauge (default is 0).
            max_v (int): The maximum value of the gauge (default is 250).
            min_v (int): The minimum value of the gauge (default is 0).
            max_angle (int): The maximum angle (in degrees) of the gauge (default is 240).
            size (int): The size of the gauge (default is 320).
            partition (int): The number of partitions in the gauge (default is 4).
            loc (tuple): The position of the gauge (default is (50, 80)).
            col_range (list): The range of colors for the gauge (default is [[255, 215, 0], [32, 178, 170]]).
        """
        super().__init__()
        self.value = value
        self.max_v = max_v
        self.min_v = min_v
        self.max_angle = max_angle
        self.size = size
        self.partition = partition
        self.loc = loc
        self.col_range = col_range
        self.tick_wid = 3
        self.arc_wid = 10
        self.value_var = IntVar()  # Variable to store value entered by user
        self.initUI()

    def initUI(self):
        """Initialize the graphical user interface (GUI) of the gauge."""
        self.master.title("Gauge")
        self.pack(fill=BOTH, expand=1)
        self.drawTop()  # Draw the top part of the gauge
        self.drawBottom()  # Draw the bottom part of the gauge

    def setValue(self, value):
        """
        Set the value of the gauge and update the display.

        Args:
            value (int): The new value of the gauge.
        """
        self.value = value
        self.canvas.delete("pointer")
        self.canvas.delete("display_box")
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def drawArc(self, loc, size, start_angle, angle, color, wid):
        """
        Draw an arc on the canvas.

        Args:
            loc (tuple): Top-left corner coordinates of the bounding box of the arc.
            size (int): Size of the bounding box (width and height) of the arc.
            start_angle (int): Starting angle of the arc (in degrees).
            angle (int): Angle to sweep (in degrees).
            color (str): Color of the arc.
            wid (int): Width of the arc.
        """
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
        """
        Draw a tick mark on the gauge.

        Args:
            value (int): Value corresponding to the tick mark.
            len (int): Length of the tick mark.
            wid (int): Width of the tick mark.
            offset (int): Offset of the tick mark from the center of the gauge.
        """
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
        self.canvas.create_line(up_x, up_y, down_x, down_y, width=wid, fill="#2b2d42")
        tag_x, tag_y = self.getLocOnArc(
            x_center, y_center, self.size / 2 + offset - len - 15, theta
        )
        self.canvas.create_text(
            tag_x, tag_y, text=round(value), font=("Helvetica", 12, "italic")
        )

    def drawPointer(self, value):
        """
        Draw the pointer of the gauge.

        Args:
            value (int): Value corresponding to the pointer position.
        """
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
        """
        Draw the pivot of the gauge.

        Args:
            x (int): x-coordinate of the pivot.
            y (int): y-coordinate of the pivot.
            size (int): Size of the pivot.
            color (str): Color of the pivot.
        """
        self.canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=color,
            outline="",
        )

    def drawDisplay(self, value):
        """
        Draw the display of the gauge.

        Args:
            value (int): Value to be displayed.
        """
        section = (
            self.partition
            - 1
            - (value - self.min_v) * self.partition // (self.max_v - self.min_v)
        )  # which section does the value located on the gauge
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
        """Draw the top part of the gauge."""
        frame = Frame(self)
        frame.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.75)
        self.canvas = Canvas(frame)
        self.canvas.pack(fill=BOTH, expand=1)
        self.color_set = generateColors(self.col_range, self.partition - 1)
        self.canvas.create_text(
            self.loc[0] + self.size / 2,
            self.loc[1] - 30,
            text="GAUGE",
            font=("Helvetica", 12, "bold"),
        )
        for i in range(self.partition):
            self.drawArc(
                self.loc,
                self.size,
                self.max_angle / self.partition * i - (self.max_angle - 180) / 2,
                self.max_angle / self.partition,
                self.color_set[i],
                self.arc_wid,
            )
        for i in range(self.partition):
            self.drawTick(
                self.max_v / self.partition * i,
                self.arc_wid * 2,
                self.tick_wid,
                self.arc_wid / 2,
            )
        self.drawTick(self.min_v, self.arc_wid * 2, self.tick_wid, self.arc_wid / 2)
        self.drawTick(self.max_v, self.arc_wid * 2, self.tick_wid, self.arc_wid / 2)
        self.drawPointer(self.value)
        self.drawDisplay(self.value)

    def drawBottom(self):
        """Draw the bottom part of the gauge."""

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
            self.arc_wid = random.randint(3, 30)
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
        """
        Get the coordinates of a point on an arc.

        Args:
            center_x (int): x-coordinate of the center of the arc.
            center_y (int): y-coordinate of the center of the arc.
            r (int): Radius of the arc.
            theta (int): Angle (in degrees) of the point on the arc.

        Returns:
            tuple: The (x, y) coordinates of the point on the arc.
        """
        theta = radians(theta)
        x = r * cos(theta) + center_x
        y = center_y - r * sin(theta)  # Invert y due to Tkinter's coordinate system
        return x, y


def hexColor(rgb):
    """
    Convert an RGB color to hexadecimal format.

    Args:
        rgb (list): List containing the RGB values.

    Returns:
        str: Hexadecimal representation of the RGB color.
    """
    red = int(rgb[0])
    green = int(rgb[1])
    blue = int(rgb[2])
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)


def generateColors(c_range, steps):
    """
    Generate a list of colors between two given RGB colors.

    Args:
        c_range (list): List containing the start and end RGB colors.
        steps (int): Number of steps to generate between the start and end colors.

    Returns:
        list: List of hexadecimal color codes.
    """
    colors = []
    colors.append(hexColor(c_range[0]))
    red = c_range[0][0]
    green = c_range[0][1]
    blue = c_range[0][2]
    for i in range(steps):
        red += (c_range[-1][0] - c_range[0][0]) / steps
        green += (c_range[-1][1] - c_range[0][1]) / steps
        blue += (c_range[-1][2] - c_range[0][2]) / steps
        colors.append(hexColor([red, green, blue]))
    colors.append(hexColor(c_range[-1]))
    return colors


def generateRandomColor():
    """Generate a random RGB color."""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return [red, green, blue]


if __name__ == "__main__":
    root = Tk()
    root.geometry("440x600+300+300")
    gauge = Gauge()
    root.mainloop()
