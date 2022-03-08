from datetime import datetime as date
from random import Random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from typing import Text

from controller.product import ProductController
from controller.provider import ProviderController
from controller.sale import SaleController
from controller.user import UserController
from extra.random import RandomObjectInfo
from model.classes.product import Clothing, Electronic, Food, Home_Appliance, Product
from model.classes.user import Customer, Seller
from view.output import TextOutput
from view.window import CenterWindow


class GUI:
    def __init__(self, db: str = "app.db"):
        self.root: tk.Tk = tk.Tk()
        self.db = db
        self.init_ui()
        self.root.mainloop()

    def init_ui(self):
        self.root.title("Loja de Departamento")
        self.root.geometry("600x400")
        self.root.configure(background="#ffffff")
        CenterWindow(self.root)
        # Protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Escape>", lambda: self.on_closing)

        self.init_menu()

    def on_closing(self):
        # if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
        self.root.destroy()

    def init_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.file_menu(menubar)
        self.user_menu(menubar)
        self.product_menu(menubar)
        # self.provider_menu(menubar)
        # self.sale_menu(menubar)

    def file_menu(self, menubar):
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Sair", command=self.on_closing)
        menubar.add_cascade(label="Programa", menu=self.filemenu)

    def user_menu(self, menubar):
        self.usermenu = tk.Menu(menubar, tearoff=0)
        userui = UserUI(self.root, self.db)

        #### ADDS ####
        add_menu = tk.Menu(menubar, tearoff=0)
        add_customer = userui.add_customer
        add_menu.add_command(label="Cliente", command=add_customer)
        add_seller = userui.add_seller
        add_menu.add_command(label="Vendedor", command=add_seller)

        ##### GETS ####
        get_menu = tk.Menu(menubar, tearoff=0)
        all_customers = userui.get_all_customers
        get_menu.add_command(label="Todos os clientes", command=all_customers)
        golden = userui.get_all_golden_customers
        get_menu.add_command(label="Clientes ouro", command=golden)
        all_sellers = userui.get_all_sellers
        get_menu.add_command(label="Todos os vendedores", command=all_sellers)
        bseller = userui.get_best_seller_of_the_month
        get_menu.add_command(label="Melhor vendedor do mês", command=bseller)

        ##### CASCADES ####
        self.usermenu.add_cascade(label="Consultar", menu=get_menu)
        self.usermenu.add_cascade(label="Cadastrar", menu=add_menu)
        menubar.add_cascade(label="Usuários", menu=self.usermenu)

    def product_menu(self, menubar):
        product_menu = tk.Menu(menubar, tearoff=0)
        pUI = ProductUI(self.root, self.db)

        add_menu = tk.Menu(menubar, tearoff=0)
        add_menu.add_command(label="Alimento", command=pUI.add_food)
        add_menu.add_command(label="Vestuário", command=pUI.add_clothing)
        add_menu.add_command(label="Eletrônico", command=pUI.add_electronic)
        add_menu.add_command(label="Eletrodoméstico", command=pUI.add_home_appliance)
        ##### GETS ####
        get_menu = tk.Menu(menubar, tearoff=0)
        products = pUI.get_all_products
        get_menu.add_command(label="Todos os produtos", command=products)
        foods = pUI.get_all_foods
        get_menu.add_command(label="Alimentos", command=foods)
        clothes = pUI.get_all_clothes
        get_menu.add_command(label="Vestuários", command=clothes)
        electronics = pUI.get_all_electronics
        get_menu.add_command(label="Eletrônicos", command=electronics)
        home_appliances = pUI.get_all_home_appliances
        get_menu.add_command(label="Eletrodomésticos", command=home_appliances)

        ##### CASCADES ####
        product_menu.add_cascade(label="Consultar", menu=get_menu)
        product_menu.add_cascade(label="Cadastrar", menu=add_menu)
        menubar.add_cascade(label="Produtos", menu=product_menu)

    def provider_menu(self, menubar):
        self.providermenu = tk.Menu(menubar, tearoff=0)
        providerui = ProviderUI(self.root, self.db)

        #### ADDS ####
        add_menu = tk.Menu(menubar, tearoff=0)
        add_provider = providerui.add_provider
        add_menu.add_command(label="Fornecedor", command=add_provider)

        ##### GETS ####
        get_menu = tk.Menu(menubar, tearoff=0)
        all_providers = providerui.get_all_providers
        get_menu.add_command(label="Todos os fornecedores", command=all_providers)

        ##### CASCADES ####
        self.providermenu.add_cascade(label="Consultar", menu=get_menu)
        self.providermenu.add_cascade(label="Cadastrar", menu=add_menu)
        menubar.add_cascade(label="Fornecedores", menu=self.providermenu)

    def sale_menu(self, menubar):
        self.salemenu = tk.Menu(menubar, tearoff=0)
        saleui = SaleUI(self.root, self.db)

        #### ADDS ####
        add_menu = tk.Menu(menubar, tearoff=0)
        add_sale = saleui.add_sale
        add_menu.add_command(label="Venda", command=add_sale)

        ##### GETS ####
        get_menu = tk.Menu(menubar, tearoff=0)
        all_sales = saleui.get_all_sales
        get_menu.add_command(label="Todas as vendas", command=all_sales)

        ##### CASCADES ####
        self.salemenu.add_cascade(label="Consultar", menu=get_menu)
        self.salemenu.add_cascade(label="Cadastrar", menu=add_menu)
        menubar.add_cascade(label="Vendas", menu=self.salemenu)


class UserUI:
    def __init__(self, root: tk.Tk, db="app.db"):
        self.root = root
        self.db = db
        self.userc = UserController(db)

    def add_customer(self):
        self.role = "customer"
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Cliente")
        gui.geometry("420x200")
        CenterWindow(gui)
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
        # padding at top
        tk.Label(gui, text="").grid(row=0, column=0, columnspan=2)
        # fields
        for field in fields:
            index = fields.index(field)  # index of field
            # Name of field
            label = tk.Label(gui, text=field, width=20, anchor="w")
            label.grid(row=index + 1, column=0)
            # Entry of field
            self.entries[field] = ttk.Entry(gui, width=30)
            self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
            self.entries[field].insert(0, placeholders[index])
            # Focus on first field
            if index == 0:
                self.entries[field].focus()

        btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
        btn.grid(row=len(fields) + 2, column=1, sticky=tk.W, pady=10)

    def add_seller(self):
        self.role = "seller"
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Vendedor")
        gui.geometry("420x280")
        CenterWindow(gui)
        fields = (
            "Nome",
            "CPF",
            "RG",
            "Data de Nascimento",
            "Endereço",
            "CEP",
            "Email",
            "Salário",
            "PIS",
            "Data de Admissão",
        )
        [
            name,
            cpf,
            rg,
            birth_date,
            address,
            zip_code,
            email,
            salary,
            pis,
            admission_date,
        ] = RandomObjectInfo(self.db, self.db, self.db).Seller()
        placeholders = (
            name,
            cpf,
            rg,
            str(birth_date)[:10],
            address,
            zip_code,
            email,
            salary,
            pis,
            str(admission_date)[:10],
        )
        self.entries = {}
        # padding at top
        tk.Label(gui, text="").grid(row=0, column=0, columnspan=2)

        for field in fields:
            index = fields.index(field)  # index of field
            # Name of field
            label = tk.Label(gui, text=field, width=20, anchor="w")
            label.grid(row=index + 1, column=0)
            # Entry of field
            self.entries[field] = ttk.Entry(gui, width=30)
            self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
            self.entries[field].insert(0, placeholders[index])
            # Focus on first field
            if index == 0:
                self.entries[field].focus()

        btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
        btn.grid(row=len(fields) + 2, column=1, sticky=tk.W, pady=10)

    def get_all_customers(self):
        customer = UserController(self.db).get_all_customers()
        if customer:
            TextOutput(self.root).display(customer, "Clientes")
        else:
            messagebox.showinfo("Aviso", "Nenhum cliente cadastrado")

    def get_all_sellers(self):
        seller = UserController(self.db).get_all_sellers()
        if seller:
            TextOutput(self.root).display(seller, "Vendedores")
        else:
            messagebox.showinfo("Aviso", "Nenhum vendedor cadastrado")

    def get_best_seller_of_the_month(self):
        def show(seller):
            if seller:
                seller, total = seller
                text = f"Vendedor: {seller}\nQuantidade de vendas: {total}"
                TextOutput(self.root).display(text, "Melhor vendedor do mês")
            else:
                messagebox.showinfo(
                    "Aviso",
                    "Nenhum vendedor cadastrado ou venda realizada neste período.",
                )

        def parse_date(datetime: str, format: str) -> date:
            try:
                return date.strptime(datetime, format)
            except ValueError:
                messagebox.showerror("Erro", "Data inválida")

        gui = tk.Toplevel(self.root)
        gui.title("Relatório Mensal")
        gui.geometry("400x125")
        CenterWindow(gui)

        tk.Label(gui, text="Mês (AAAA-MM)").pack(pady=10)
        self.month = tk.Entry(gui, width=30)
        self.month.insert(0, date.today().strftime("%Y-%m"))
        self.month.pack()

        def show_employee():
            mm, yy = self.month.get(), self.month.get()
            show(
                UserController(self.db).get_best_seller_of_the_month(
                    str(parse_date(mm, "%Y-%m").month),
                    str(parse_date(yy, "%Y-%m").year),
                )
            )

        btn = tk.Button(
            gui,
            text="Gerar Relatório",
            command=show_employee,
        )
        btn.pack(pady=10)

    def get_all_golden_customers(self):
        customers = UserController(self.db).get_all_golden_customers()
        if customers:
            TextOutput(self.root).display(customers, "Clientes Ouro")
        else:
            messagebox.showinfo("Aviso", "Nenhum cliente ouro cadastrado")

    def try_insert(self):
        errors = self.validate_user_entries()
        if len(errors) > 0:
            for error in errors:
                messagebox.showerror("Erro", error)

        else:
            if self.role == "seller":
                self.userc.add_user(
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
                self.userc.add_user(
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


class ProductUI:
    def __init__(self, root: tk.Tk, db: str = "app.db"):
        self.root: tk.Tk = root
        self.db: str = db

    def add_product(self, type: str):
        self.type = type
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Cliente")
        gui.geometry("450x260")
        CenterWindow(gui)
        fields = (
            "Nome",
            "Descrição",
            "Data de Fabricação",
            "Preço",
            "Está disponível? [Sim/Não]",
        )
        RandomObject = RandomObjectInfo(self.db, self.db, self.db)
        product = None
        if self.type == "food":
            product = RandomObject.Food()
        elif self.type == "clothing":
            product = RandomObject.Clothing()
        elif self.type == "electronic":
            product = RandomObject.Electronic()
        elif self.type == "home appliance":
            product = RandomObject.HomeAppliance()
        [
            name,
            description,
            fabrication,
            price,
            _,
            is_available,
        ] = product

        placeholders = (
            name,
            description,
            str(fabrication)[:10],
            price,
            "Sim" if is_available else "Não",
        )
        self.entries = {}
        # padding at top
        tk.Label(gui, text="").grid(row=0, column=0, columnspan=2)
        # fields
        for field in fields:
            index = fields.index(field)  # index of field
            # Name of field
            label = tk.Label(gui, text=field, width=25, anchor="w")
            label.grid(row=index + 1, column=0)
            # Entry of field
            self.entries[field] = ttk.Entry(gui, width=30)
            self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
            self.entries[field].insert(0, placeholders[index])
            # Focus on first field
            if index == 0:
                self.entries[field].focus()

        label = tk.Label(gui, text="Fornecedor", width=25, anchor="w")
        label.grid(row=len(fields) + 2, column=0)
        self.provider = tk.StringVar(gui)
        providers = ProviderController(self.db).get_all_providers()
        display = lambda p: f"{p.get_id()} - {p.get_name()} - {p.get_cnpj()}"
        self.provider.set(display(providers[0]))
        op = tk.OptionMenu(gui, self.provider, *[display(p) for p in providers])
        op.config(width=25)
        op.grid(row=len(fields) + 2, column=1)

        btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
        btn.grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)

    def add_food(self):
        self.add_product("food")

    def add_clothing(self):
        self.add_product("clothing")

    def add_electronic(self):
        self.add_product("electronic")

    def add_home_appliance(self):
        self.add_product("home appliance")

    def get_all_products(self):
        products = ProductController(self.db).get_all_products()
        if products:
            TextOutput(self.root).display(products, "Produtos")
        else:
            messagebox.showinfo("Aviso", "Não há produtos cadastrados")

    def get_all_foods(self):
        products = ProductController(self.db).get_all_foods()
        if products:
            TextOutput(self.root).display(products, "Alimentos")
        else:
            messagebox.showinfo("Aviso", "Não há alimentos cadastrados")

    def get_all_clothes(self):
        products = ProductController(self.db).get_all_clothes()
        if products:
            TextOutput(self.root).display(products, "Roupas")
        else:
            messagebox.showinfo("Aviso", "Não há roupas cadastradas")

    def get_all_electronics(self):
        products = ProductController(self.db).get_all_electronics()
        if products:
            TextOutput(self.root).display(products, "Eletrônicos")
        else:
            messagebox.showinfo("Aviso", "Não há eletrônicos cadastrados")

    def get_all_home_appliances(self):
        products = ProductController(self.db).get_all_home_appliances()
        if products:
            TextOutput(self.root).display(products, "Eletrodomésticos")
        else:
            messagebox.showinfo("Aviso", "Não há eletrodomésticos cadastrados")

    def try_insert(self):
        errors = self.validate_fields()
        if errors:
            messagebox.showinfo("Erro", "\n".join(errors))
        else:
            c = ProductController(self.db)
            pc = ProviderController(self.db)
            provider = pc.get_provider_by_id(self.provider.get().split(" - ")[0])
            if self.type == "food":
                c.add_product(
                    Food(
                        self.entries["Nome"].get(),
                        self.entries["Descrição"].get(),
                        self.entries["Data de Fabricação"].get(),
                        self.entries["Preço"].get(),
                        provider,
                        self.entries["Está disponível? [Sim/Não]"].get(),
                    )
                )
            elif self.type == "clothing":
                c.add_product(
                    Clothing(
                        self.entries["Nome"].get(),
                        self.entries["Descrição"].get(),
                        self.entries["Data de Fabricação"].get(),
                        self.entries["Preço"].get(),
                        provider,
                        self.entries["Está disponível? [Sim/Não]"].get(),
                    )
                )
            elif self.type == "electronic":
                c.add_product(
                    Electronic(
                        self.entries["Nome"].get(),
                        self.entries["Descrição"].get(),
                        self.entries["Data de Fabricação"].get(),
                        self.entries["Preço"].get(),
                        provider,
                        self.entries["Está disponível? [Sim/Não]"].get(),
                    )
                )
            elif self.type == "home appliance":
                c.add_product(
                    Home_Appliance(
                        self.entries["Nome"].get(),
                        self.entries["Descrição"].get(),
                        self.entries["Data de Fabricação"].get(),
                        self.entries["Preço"].get(),
                        provider,
                        self.entries["Está disponível? [Sim/Não]"].get(),
                    )
                )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
            self.root.destroy()

    def validate_fields(self):
        errors = []
        for field in self.entries:
            if not self.entries[field].get():
                errors.append(f"O campo {field} não pode estar vazio")
        return errors


class ProviderUI:
    def __init__(self, root, db):  # TODO FAZ ISSO
        pass

    def add_provider(self):  # TODO FAZE ISSO TBM
        pass

    def get_al_providers(self):
        provider = ProviderController(self.db).get_all_providers()
        if provider:
            TextOutput(self.root).display(provider, "Todos os provedores")
        else:
            messagebox.showinfo("Aviso", "não há provedores cadastrados")

    def get_provider_by_id(self, id: int):
        provider = ProviderController(self.db).get_provider_by_id(id)
        if provider:
            TextOutput(self.root).display(provider, "Provedor com o id", id)
        else:
            messagebox.showinfo("Aviso", "não existe um provedor com o id", id)

    def get_random_provider(self):
        provider = ProviderController(self.db).get_random_provider()
        if provider:
            TextOutput(self.root).display(
                provider, "Provedor selecionado aleatoriamente"
            )
        else:
            messagebox.showinfo(
                "Aviso", "não foi possivel selecionar um provedor aleatoriamente"
            )


class SaleUI:
    def __init__(self, root, db):
        pass

    def get_all_sales(self):
        sale = SaleController(self.db).get_all_sales()
        if sale:
            TextOutput(self.root).display(sale, "Todas as vendas realizadas")
        else:
            messagebox.showinfo("Aviso", "não existem vendas cadastradas")

    def get_sale_by_id(self, id: int):
        sale = SaleController(self.db).get_sale_by_id(id)
        if sale:
            TextOutput(self.db).display(sale, "Venda com o id:", id)
        else:
            messagebox.showinfo("aviso", "não existe uma venda com o id:", id)

    def get_sale_and_profit_of_month(self, month, year):
        sale = SaleController(self.db).get_all_sales_in_month(month, year)
        if sale:
            TextOutput(self.db).display(
                sale, "vendas e lucro do mês", month, "no ano", year
            )
        else:
            messagebox.showinfo(
                "Aviso", "não foi possivel encontrar vendas na data selecionada"
            )

    def get_all_sales_paid_via_card(self):
        sale = SaleController(self.db).get_all_sales_paid_via_card()
        if sale:
            TextOutput(self.db).display(
                sale, "Todas as vendas realizadas com cartão de crédito"
            )
        else:
            messagebox.showinfo(
                "Aviso", "Não foram realizadas vendas com o cartão de crédito"
            )
