from tkinter import BOTH, Tk
from gauge import Gauge


def main():
    root = Tk()
    root.geometry("400x250+300+300")
    root.title("Data Display")
    gauge = Gauge()
    gauge.setValue(100)
    gauge.pack(fill=BOTH, expand=1)
    root.mainloop()


if __name__ == "__main__":
    main()
