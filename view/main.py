from datetime import datetime as date
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from controller.product import ProductController
from controller.provider import ProviderController
from controller.sale import SaleController
from controller.user import UserController
from extra.random import RandomObjectInfo
from model.classes.user import Customer, Seller


class MainView:
    def __init__(self, db: str = "app.db"):
        self.root: tk.Tk = tk.Tk()
        self.db = db
        self.productc = ProductController(db)
        self.providerc = ProviderController(db)
        self.salec = SaleController(db)
        self.userc = UserController(db)
        self.init_ui()
        self.root.mainloop()

    def init_ui(self):
        self.root.title("Loja de Departamento")
        self.root.geometry("600x400")
        self.root.configure(background="#ffffff")
        # Protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Escape>", lambda: self.on_closing)

        self.init_menu()
        # self.init_widgets()

    def init_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # FILE MENU
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Sair", command=self.on_closing)
        menubar.add_cascade(label="Programa", menu=self.filemenu)

        # USER MENU
        self.usermenu = tk.Menu(menubar, tearoff=0)
        self.add_user_menu = tk.Menu(menubar, tearoff=0)
        self.add_user_menu.add_command(
            label="Cliente", command=UserUI(self.root, self.db).add_customer
        )
        self.add_user_menu.add_command(
            label="Vendedor", command=UserUI(self.root, self.db).add_seller
        )
        self.get_user_menu = tk.Menu(menubar, tearoff=0)
        self.get_user_menu.add_command(
            label="Todos os clientes", command=UserUI(self.root, self.db).get_customers
        )
        self.get_user_menu.add_command(
            label="Todos os vendedores", command=UserUI(self.root, self.db).get_sellers
        )
        self.usermenu.add_cascade(label="Consultar", menu=self.get_user_menu)
        self.usermenu.add_cascade(label="Cadastrar", menu=self.add_user_menu)
        menubar.add_cascade(label="Usuários", menu=self.usermenu)

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.root.destroy()


class UserUI:
    def __init__(self, root: tk.Tk, db="app.db"):
        self.root = root
        self.db = db
        self.userc = UserController(db)

    def add_customer(self):
        self.role = "customer"
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Cliente")
        gui.geometry("420x290")
        fields = (
            "Nome",
            "CPF",
            "RG",
            "Data de Nascimento",
            "Endereço",
            "CEP",
            "Email",
            "Cliente Ouro [Sim/Não]",
        )
        [
            name,
            cpf,
            rg,
            birth_date,
            address,
            zip_code,
            email,
            is_golden_client,
        ] = RandomObjectInfo(self.db, self.db, self.db).Customer()
        placeholders = (
            name,
            cpf,
            rg,
            str(birth_date)[:10],
            address,
            zip_code,
            email,
            "Sim" if is_golden_client else "Não",
        )
        self.entries = {}
        # add a padding in the top
        space = tk.Frame(gui, height=15)
        space.grid(row=1, column=0)

        # fields
        for field in fields:
            tk.Label(gui, text=field, width=20, anchor="w").grid(
                row=fields.index(field) + 2, column=0
            )
            self.entries[field] = ttk.Entry(gui, width=30)
            self.entries[field].grid(
                row=(fields.index(field) + 2), column=1, sticky=tk.W
            )
            self.entries[field].insert(0, placeholders[fields.index(field)])
            if fields.index(field) == 0:
                self.entries[field].focus()
            btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
            btn.grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)

    def add_seller(self):
        root = tk.Toplevel(self.root)
        root.title("Cadastro de Vendedor")
        tk.Label(root, text="Nome").grid(row=0, column=0)

    def get_customers(self):
        root = tk.Toplevel(self.root)
        root.title("Consultar Clientes")
        tk.Label(root, text="Nome").grid(row=0, column=0)

    def get_sellers(self):
        root = tk.Toplevel(self.root)
        root.title("Consultar Vendedores")
        tk.Label(root, text="Nome").grid(row=0, column=0)

    def try_insert(self):
        errors = self.validate_user_entries()
        if len(errors) > 0:
            for error in errors:
                messagebox.showerror("Erro", error)

        else:
            if self.role == "seller":
                self.userc.insert_user(
                    Seller(
                        self.entries["Nome"].get(),
                        str(self.entries["CPF"].get()),
                        str(self.entries["RG"].get()),
                        date.strptime(
                            self.entries["Data de Nascimento"].get(), "%Y-%m-%d"
                        ),
                        self.entries["Endereço"].get(),
                        str(self.entries["CEP"].get()),
                        self.entries["Email"].get(),
                        float(self.entries["Salário"].get()),
                        str(self.entries["PIS"].get()),
                        date.strptime(
                            self.entries["Data de Admissão"].get(), "%Y-%m-%d"
                        ),
                    )
                )
            elif type == "customer":
                self.userc.insert_user(
                    Customer(
                        self.entries["Nome"].get(),
                        str(self.entries["CPF"].get()),
                        str(self.entries["RG"].get()),
                        date.strptime(
                            self.entries["Data de Nascimento"].get(), "%Y-%m-%d"
                        ),
                        self.entries["Endereço"].get(),
                        str(self.entries["CEP"].get()),
                        self.entries["Email"].get(),
                        self.entries["Cliente Ouro [Sim/Não]"].get().upper() == "Sim",
                    )
                )
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

    def validate_user_entries(self):
        errors = []
        name = self.entries["Nome"].get()
        for i in range(len(name)):
            if name[i].isdigit():
                errors.append("Nome não pode conter números")
                break
        if len(name) < 3:
            errors.append("Nome deve conter no mínimo 3 caracteres")

        cpf = self.entries["CPF"].get()
        if len(cpf) != 11:
            errors.append("CPF deve conter 11 caracteres")
        for i in range(len(cpf)):
            if not cpf[i].isdigit():
                errors.append("CPF deve conter apenas números")
                break
        rg = self.entries["RG"].get()
        if len(rg) != 9:
            errors.append("RG deve conter 9 caracteres")
        for i in range(len(rg)):
            if not rg[i].isdigit():
                errors.append("RG deve conter apenas números")
                break

        birth_date = self.entries["Data de Nascimento"].get()
        if birth_date is None:
            errors.append("Data de Nascimento não pode ser vazia")
        if len(birth_date) != 10:
            errors.append("Data de Nascimento deve conter 10 caracteres")
        if birth_date[4] != "-" or birth_date[7] != "-":
            errors.append("Data de Nascimento deve estar no formato AAAA-MM-DD")

        address = self.entries["Endereço"].get()
        if len(address) < 5:
            errors.append("Endereço deve conter no mínimo 5 caracteres")

        zip_code = self.entries["CEP"].get()
        if len(zip_code) != 9:
            errors.append("CEP deve conter 9 caracteres")

        email = self.entries["Email"].get()
        if email is None:
            errors.append("Email cannot be empty")
        if "@" not in email:
            errors.append("Email must contain @")
        if "." not in email:
            errors.append("Email must contain .")
        if email.count("@") > 1:
            errors.append("Email must contain only one @")

        if self.role == "seller":

            salary = self.entries["Salário"].get()
            if salary is None:
                errors.append("Salário não pode ser vazio")
            if len(salary) < 3:
                errors.append("Salário deve conter no mínimo 3 caracteres")
            for i in range(len(salary)):
                if not salary[i].isdigit() and salary[i] != "." and salary[i] != ",":
                    errors.append("Salário deve conter apenas números")
                    break
            if salary[-1] == "." or salary[-1] == ",":
                errors.append("Salário deve conter apenas números")

            pis = self.entries["PIS"].get()
            if len(pis) != 11:
                errors.append("PIS deve conter 11 caracteres")

            admission_date = self.entries["Data de Admissão"].get()
            if len(admission_date) != 10:
                errors.append("Data de Admissão deve conter 10 caracteres")
            try:
                aux = date.strptime(admission_date, "%Y-%m-%d")
                if aux > date.now():
                    errors.append(
                        "Data de Admissão não pode ser maior que a data atual"
                    )
            except:
                errors.append("Data de Admissão deve estar no formato AAAA-MM-DD")

        if self.role == "customer":
            is_golden_client = self.entries["Cliente Ouro [Sim/Não]"].get()
            if is_golden_client is None:
                errors.append("Cliente Ouro não pode ser vazio")
            if len(is_golden_client) != 3:
                errors.append("Cliente Ouro deve preenchido com Sim ou Não")
            if is_golden_client not in ["Sim", "Não"]:
                errors.append("Cliente Ouro deve preenchido com Sim ou Não")
        return errors
