import tkinter as tk
from view.window import CenterWindow


class TextOutput:
    def __init__(self, root: tk.Tk):
        self.root = root

    def display(self, text, title="Renterio - Sistema de locação de veículos"):
        self.text = text
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.title(title)
        self.toplevel.geometry("700x360")
        self.toplevel.resizable(False, False)
        CenterWindow(self.toplevel)

        self.text_box_gui(self.toplevel)

    def text_box_gui(self, root):
        tex = tk.Text(master=root)
        tex.pack(side=tk.RIGHT)
        bop = tk.Frame(master=root)
        bop.pack(side=tk.LEFT)
        tk.Button(bop, text="Mostrar", command=self.cbc(self.text, tex)).pack(
            side=tk.TOP
        )
        tk.Button(bop, text="Fechar", command=root.destroy).pack(side=tk.BOTTOM)

    def cbc(self, text, tex):
        return lambda: self.callback(text, tex)

    def callback(self, text, tex):
        s = "Nada a mostrar"
        if text is not None:
            if isinstance(text, str):
                s = str(text)
            else:
                s = ""
                iterator = iter(text)
                while True:
                    try:
                        s += str(next(iterator)) + "\n\n"
                    except StopIteration:
                        break

        tex.insert(tk.END, s)
        tex.see(tk.END)
