# from tkinter import BOTH, Tk
# from bar import Bar
# from gauge import Gauge


# def main():
# root = Tk()
# root.geometry("800x500+300+300")
# root.title("Data Display")
# gauge = Gauge()
# gauge.setValue(50)
# gauge.pack(fill=BOTH, expand=1)
# # bar = Bar()
# # bar.setValue(50)
# # bar.grid(row=0, column=1, sticky="nsew")
# root.mainloop()

from panel import Panel

if __name__ == "__main__":
    panel = Panel()
    panel.mainloop()
