from tkinter import Canvas


class Bar(Canvas):
    def __init__(
        self,
        value=0,
        loc=(200, 80),
    ):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.create_line(500, 80, 550, 350)

    def setValue(self, value):
        pass
