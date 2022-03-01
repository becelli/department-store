import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MainView:
    def __init__(self, db: str = "app.db"):
        self.root: tk.Tk = tk.Tk()
        self.init_ui()
        self.root.mainloop()

    def init_ui(self):
        self.root.tk_setPalette(
            background="#40E0D0",
            foreground="black",
            activeBackground="black",
            activeForeground="white",
        )
        self.root.button = tk.Button(self.root, text="Press me!").pack()

        self.root.title("Loja de Departamento")
        self.root.geometry("1280x720")
        self.root.configure(background="SystemButtonFace")

        # Protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Escape>", lambda e: self.on_closing())

        self.init_menu()
        self.init_widgets()

    def init_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Sair", command=self.on_closing)
        menubar.add_cascade(label="Programa", menu=self.filemenu)

        self.helpmenu = tk.Menu(menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.on_about)
        menubar.add_cascade(label="Help", menu=self.helpmenu)

    def init_widgets(self):
        self.lbl_title = ttk.Label(self.root, text="Main")
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky="we")

        self.btn_add = ttk.Button(self.root, text="Add", command=self.on_add)
        self.btn_add.grid(row=1, column=0, sticky="we")

        self.btn_edit = ttk.Button(self.root, text="Edit", command=self.on_edit)
        self.btn_edit.grid(row=1, column=1, sticky="we")

        self.btn_delete = ttk.Button(self.root, text="Delete", command=self.on_delete)
        self.btn_delete.grid(row=2, column=0, sticky="we")

        self.btn_view = ttk.Button(self.root, text="View", command=self.on_view)
        self.btn_view.grid(row=2, column=1, sticky="we")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def on_add(self):
        pass

    def on_edit(self):
        pass

    def on_delete(self):
        pass

    def on_view(self):
        pass

    def on_about(self):
        pass
