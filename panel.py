from tkinter import *
from gauge import Gauge
from bar import Bar


class Panel(Tk):
    def __init__(self):
        super().__init__()
        Canvas(self, width=800, height=500).pack()
        self.container = Frame(self)
        self.container["relief"] = "ridge"
        self.container.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.initUI()

    def initUI(self):
        self.gauge = Gauge()
        self.gauge.setValue(50)
        self.gauge.place(relx=0.25, rely=0.008, relwidth=0.45, relheight=0.96)
        self.bar = Bar()
        self.bar.setValue(50)
        self.gauge.place(relx=0.55, rely=0.008, relwidth=0.45, relheight=0.96)

    def create_vars(self):
        self.value = IntVar()
