"""Compatibility entry point for the SmartCalc Pro application."""

import tkinter as tk

from main import SmartCalcPro


class SmartCalculator:
    """Launch the complete SmartCalc Pro interface."""

    def __init__(self):
        self.window = tk.Tk()
        self.app = SmartCalcPro(self.window)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    SmartCalculator().run()