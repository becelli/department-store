import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.parent = tk.Tk()
        self.init_ui()
        self.controller
        self.parent.mainloop()
