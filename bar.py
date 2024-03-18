from tkinter import Canvas


class Bar(Canvas):
    def _init__(
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
