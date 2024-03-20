import random
from tkinter import *
from tkinter import messagebox


class Bar(Frame):
    def __init__(
        self,
        value=0,
        max_v=250,
        min_v=0,
        height=320,
        width=180,
        cylinder_wid=0.5,
        tick_depth=5,
        loc=(50, 80),
        col_range=[[255, 215, 0], [32, 178, 170]],
    ):
        super().__init__()
        self.value = value
        self.max_v = max_v
        self.min_v = min_v
        self.height = height
        self.width = width
        self.cylinder_wid = cylinder_wid
        self.tick_depth = tick_depth
        self.loc = loc
        self.col_range = col_range
        self.value_var = IntVar()  # Variable to store value entered by user
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)
        self.drawLeft()
        self.drawRight()

    def setValue(self, value):
        pass

    def drawLeft(self):
        frame = Frame(self)
        frame.place(relx=0.03, rely=0.03, relwidth=0.7, relheight=0.94)
        self.canvas = Canvas(frame)
        self.canvas.pack(fill=BOTH, expand=1)
        self.drawTicks()
        self.drawCylinder()
        self.drawDisplay()

    def drawTicks(self):
        pass

    def drawCylinder(self):
        pass

    def drawDisplay(self):
        pass

    def drawRight(self):
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
        frame.place(relx=0.75, rely=0.03, relwidth=0.25, relheight=0.94)
        entry = Entry(frame, textvariable=self.value_var)
        entry.place(relx=0.03, rely=0.35, relwidth=0.5, relheight=0.08)
        submit_btn = Button(frame, text="UPDATE", command=handleUpdate)
        submit_btn.place(relx=0.03, rely=0.45, relwidth=0.5, relheight=0.08)
        lucky_btn = Button(frame, text="LUCKY", command=handleLucky)
        lucky_btn.place(relx=0.03, rely=0.6, relwidth=0.5, relheight=0.08)


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
    root.geometry("600x400+300+300")
    bar = Bar()
    root.mainloop()
