import tkinter as tk
from view.gui import GUI
from view.window import CenterWindow
from controller.admin import DatabaseController


class Start(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        CenterWindow(self.root)
        self.root.title("Nome do Banco de Dados")
        self.root.geometry("300x110")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="Insira o nome do banco:",
        ).pack(pady=5)
        self.entry = tk.Entry(self.root)
        self.entry.insert(0, "app.db")
        self.entry.pack(pady=5)
        tk.Button(
            self.root, text="  OK  ", command=lambda: self.main(self.entry.get())
        ).pack(pady=5, padx=5)
        self.root.mainloop()

    def main(self, db: str = "app.db"):
        self.root.destroy()
        db = "app.db" if db == "" else db
        admin = DatabaseController(db)
        admin.init_database()
        #admin.populate_database(35)
        GUI(db)
        
