from datetime import datetime as date
from email import iterators
import string
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from controller.product import ProductController
from controller.provider import ProviderController
from controller.sale import SaleController
from controller.user import UserController
from extra.random import RandomObjectInfo
from model.classes.product import Product, ProductStrategy
from model.classes.provider import Provider
from model.classes.user import Customer, Seller
from model.classes.payment import Cash, CreditCard, Pix
from model.classes.sale import Sale, SaleItem
from view.output import TextOutput
from view.window import CenterWindow



def show_errors(errors):
    if len(errors) > 0:
        iterator = iter(errors)
        while True:
            try:
                error = next(iterator)
                messagebox.showerror("Erro", error)
            except StopIteration:
                break
        return True
    return False


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
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.init_menu()

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.root.destroy()

    def init_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.file_menu(menubar)
        self.user_menu(menubar)
        self.product_menu(menubar)
        self.provider_menu(menubar)
        self.sale_menu(menubar)

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
        most_sold = pUI.get_most_sold_products
        get_menu.add_command(label="Mais Vendidos", command=most_sold)

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
        provider_info = providerui.get_provider_info
        get_menu.add_command(label="Fornecedor", command=provider_info)

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
        sale_info = saleui.get_sale_info
        get_menu.add_command(label="Venda", command=sale_info)
        paid_on_card = saleui.get_all_sales_paid_via_card
        get_menu.add_command(label="Pagamento Cartão", command=paid_on_card)
        paid_on_cash = saleui.get_all_sales_paid_via_cash
        get_menu.add_command(label="Pagamento Dinheiro", command=paid_on_cash)
        paid_on_pix = saleui.get_all_sales_paid_via_pix
        get_menu.add_command(label="Pagamento Pix", command=paid_on_pix)
        customer_history = saleui.get_customer_history
        get_menu.add_command(label="Histórico do cliente", command=customer_history)
        mensal_sales = saleui.get_monthly_sales
        get_menu.add_command(label="Vendas mensais", command=mensal_sales)

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
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Cadastro de Cliente")
        self.gui.geometry("420x240")
        CenterWindow(self.gui)
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
        tk.Label(self.gui, text="").grid(row=0, column=0, columnspan=2)
        # fields
        iterator = iter(fields)
        while True:
            try:
                field = next(iterator)
                index = fields.index(field)  # index of field
                # Name of field
                label = tk.Label(self.gui, text=field, width=20, anchor="w")
                label.grid(row=index + 1, column=0)
                # Entry of field
                self.entries[field] = ttk.Entry(self.gui, width=30)
                self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
                self.entries[field].insert(0, placeholders[index])
                # Focus on first field
                if index == 0:
                    self.entries[field].focus()
            except StopIteration:
                break

        btn = ttk.Button(self.gui, text="Cadastrar", command=lambda: self.try_insert())
        btn.grid(row=len(fields) + 2, column=1, sticky=tk.W, pady=10)

    def add_seller(self):
        self.role = "seller"
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Cadastro de Vendedor")
        self.gui.geometry("420x280")
        CenterWindow(self.gui)

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
        tk.Label(self.gui, text="").grid(row=0, column=0, columnspan=2)
        iterator = iter(fields)
        while True:
            try:
                field = next(iterator)
                index = fields.index(field)  # index of field
                # Name of field
                label = tk.Label(self.gui, text=field, width=20, anchor="w")
                label.grid(row=index + 1, column=0)
                # Entry of field
                self.entries[field] = ttk.Entry(self.gui, width=30)
                self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
                self.entries[field].insert(0, placeholders[index])
                # Focus on first field
                if index == 0:
                    self.entries[field].focus()
            except StopIteration:
                break

        btn = ttk.Button(self.gui, text="Cadastrar", command=lambda: self.try_insert())
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

        self.gui = tk.Toplevel(self.root)
        self.gui.title("Relatório Mensal")
        self.gui.geometry("400x125")
        CenterWindow(self.gui)

        tk.Label(self.gui, text="Mês (AAAA-MM)").pack(pady=10)
        self.month = tk.Entry(self.gui, width=30)
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
            self.gui,
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
        if show_errors(errors):
            return
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
            elif self.role == "customer":
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
                        self.entries["Cliente Ouro [Sim/Não]"].get().upper() == "SIM",
                    )
                )
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

    def validate_user_entries(self):
        errors = []
        name = self.entries["Nome"].get()
        iterator = iter(name)
        while True:
            try:
                char = next(iterator).upper()
                if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
                    errors.append("Nome não pode conter números")
                    break
            except StopIteration:
                break

        if len(name) < 3:
            errors.append("Nome deve conter no mínimo 3 caracteres")

        cpf = self.entries["CPF"].get()
        if len(cpf) != 11:
            errors.append("CPF deve conter 11 caracteres")

        iterator = iter(cpf)
        while True:
            try:
                char = next(iterator)
                if char not in "0123456789":
                    errors.append("CPF deve conter apenas números")
            except StopIteration:
                break

        rg = self.entries["RG"].get()
        if len(rg) != 9:
            errors.append("RG deve conter 9 caracteres")
        iterator = iter(rg)
        while True:
            try:
                if next(iterator) not in "0123456789":
                    errors.append("RG deve conter apenas números")
            except StopIteration:
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
            errors.append("Email não pode estar vazio")
        if "@" not in email:
            errors.append("Email deve conter @")
        if "." not in email:
            errors.append("Email deve conter .")
        if email.count("@") > 1:
            errors.append("Email deve conter apenas um @")

        if self.role == "seller":

            salary = self.entries["Salário"].get()
            if salary is None:
                errors.append("Salário não pode ser vazio")
            if len(salary) < 3:
                errors.append("Salário deve conter no mínimo 3 caracteres")
            iterator = iter(salary)
            while True:
                try:
                    c = next(iterator)
                    if c not in "0123456789.":
                        errors.append("Salário deve conter apenas números")
                        break
                except StopIteration:
                    break
            if salary.count(".") > 1:
                errors.append("Salário deve conter apenas um ponto")

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
            if is_golden_client.upper() not in ["SIM", "NÃO", "NAO"]:
                errors.append("Cliente Ouro deve preenchido com Sim ou Não")
        return errors


class ProductUI:
    def __init__(self, root: tk.Tk, db: str = "app.db"):
        self.root: tk.Tk = root
        self.db: str = db

    def add_product(self, type: str):
        self.type = type
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Cadastro de Produto")
        self.gui.geometry("450x200")
        CenterWindow(self.gui)
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
            product = RandomObject.Home_Appliance()
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
        tk.Label(self.gui, text="").grid(row=0, column=0, columnspan=2)
        # fields
        iterator = iter(fields)
        while True:
            try:
                field = next(iterator)
                index = fields.index(field)  # index of field
                # Name of field
                label = tk.Label(self.gui, text=field, width=20, anchor="w")
                label.grid(row=index + 1, column=0)
                # Entry of field
                self.entries[field] = ttk.Entry(self.gui, width=30)
                self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
                self.entries[field].insert(0, placeholders[index])
                # Focus on first field
                if index == 0:
                    self.entries[field].focus()
            except StopIteration:
                break

        label = tk.Label(self.gui, text="Fornecedor", width=25, anchor="w")
        label.grid(row=len(fields) + 2, column=0)
        self.provider = tk.StringVar(self.gui)
        providers = ProviderController(self.db).get_all_providers()
        display = lambda p: f"{p.get_id()} - {p.get_name()} - {p.get_cnpj()}"
        self.provider.set(display(providers[0]))
        op = tk.OptionMenu(self.gui, self.provider, *[display(p) for p in providers])
        op.config(width=25)
        op.grid(row=len(fields) + 2, column=1)

        btn = ttk.Button(self.gui, text="Cadastrar", command=lambda: self.try_insert())
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
            self._prompt_sort_method(products, "Produtos")
        else:
            messagebox.showinfo("Aviso", "Não há produtos cadastrados")

    def get_all_foods(self):
        products = ProductController(self.db).get_all_foods()
        if products:
            self._prompt_sort_method(products, "Alimentos")
        else:
            messagebox.showinfo("Aviso", "Não há alimentos cadastrados")

    def get_all_clothes(self):
        products = ProductController(self.db).get_all_clothes()
        if products:
            self._prompt_sort_method(products, "Roupas")
        else:
            messagebox.showinfo("Aviso", "Não há roupas cadastradas")

    def get_all_electronics(self):
        products = ProductController(self.db).get_all_electronics()
        if products:
            self._prompt_sort_method(products, "Eletrônicos")
        else:
            messagebox.showinfo("Aviso", "Não há eletrônicos cadastrados")

    def get_all_home_appliances(self):
        products = ProductController(self.db).get_all_home_appliances()
        if products:
            self._prompt_sort_method(products, "Eletrodomésticos")
        else:
            messagebox.showinfo("Aviso", "Não há eletrodomésticos cadastrados")

    def get_most_sold_products(self):
        products = ProductController(self.db).get_most_sold_products()
        if products:
            self._prompt_sort_method(products, "Produtos mais vendidos")
        else:
            messagebox.showinfo("Aviso", "Não há produtos mais vendidos")

    def _prompt_sort_method(self, products, title: str):
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Ordenar valores...")
        self.gui.geometry("300x100")
        CenterWindow(self.gui)

        tk.Label(self.gui, text="Escolha o método de ordenação:").grid(row=0, column=0)
        self.sort_method = tk.StringVar(self.gui)
        self.sort_method.set("Bubblesort")
        op = tk.OptionMenu(self.gui, self.sort_method, "Bubblesort", "Insertionsort")
        op.config(width=20)
        op.grid(row=1, column=0, sticky=tk.W)

        btn = ttk.Button(
            self.gui,
            text="Ordenar",
            command=lambda: self._sort_and_display(products, title),
        )
        btn.grid(row=1, column=1, sticky=tk.W, pady=10)

    def _sort_and_display(self, products, title: str):
        self.gui.destroy()
        strategy = ProductStrategy()
        if self.sort_method.get() == "Bubblesort":
            products = strategy.sort("Bubblesort", products)
        elif self.sort_method.get() == "Insertionsort":
            products = strategy.sort("Insertionsort", products)
        TextOutput(self.root).display(products, title)

    def try_insert(self):
        errors = self._validate_fields_products()
        if show_errors(errors):
            return
        else:
            c = ProductController(self.db)
            pc = ProviderController(self.db)
            provider = pc.get_provider_by_id(self.provider.get().split(" - ")[0])
            product = c.FactoryProduct(
                self.type,
                name=self.entries["Nome"].get(),
                description=self.entries["Descrição"].get(),
                fabrication_date=self.entries["Data de Fabricação"].get(),
                price=self.entries["Preço"].get(),
                provider=provider,
                is_available=self.entries["Está disponível? [Sim/Não]"].get(),
            )
            c.add_product(product)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
            self.gui.destroy()

    def _validate_fields_products(self):
        description = self.entries["Descrição"].get()
        name = self.entries["Nome"].get()
        fabrication_date = self.entries["Data de Fabricação"].get()
        price = self.entries["Preço"].get()
        avaliable = self.entries["Está disponível? [Sim/Não]"].get()
        errors = []

        # validar nome
        if name is None:
            errors.append("Nome não deve estar vazio")
        if len(name) < 2:
            errors.append("Nome deve conter no mínimo 2 caracteres")
        if len(name) > 50:
            errors.append("Nome deve conter no máximo 50 caracteres")

        # validar disponível
        if avaliable is None:
            errors.append("Selecione ao menos uma das opções")
        if avaliable not in ["Sim", "Não"]:
            errors.append("Selecione ao menos uma das opções: Sim ou Não")

        # validar preço
        if price is None:
            errors.append("Preço não pode estar vazio")
        try:
            float(price)
        except ValueError:
            errors.append("Preço deve ser um número")
        # validar descrição
        if description is None:
            errors.append("Descrição não pode estar vazia")
        if len(description) < 3:
            errors.append("Descrição deve conter no mínimo 3 caracteres")
        if len(description) > 500:
            errors.append("Descrição deve conter no máximo 500 caracteres")

        # validar data de fabricação
        if fabrication_date is None:
            errors.append("Data de fabricação não pode ser vazia")
        if len(fabrication_date) != 4:
            errors.append("Data de fabricação deve conter 4 caracteres")
        try:
            date.strptime(fabrication_date, "%Y")
        except ValueError:
            errors.append("Data de fabricação deve estar no formato AAAA")

        return errors


class ProviderUI:
    def __init__(self, root: tk.Tk, db: str = "app.db"):
        self.root: tk.Tk = root
        self.db = db

    def add_provider(self):
        self.role = "provider"
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Cadastro de Provedor")
        self.gui.geometry("420x200")
        CenterWindow(self.gui)
        fields = (
            "CNPJ",
            "Nome",
            "Descrição",
            "Email",
            "Telefone",
            "Endereço",
        )
        [cnpj, name, description, email, phone, address] = RandomObjectInfo(
            self.db, self.db, self.db
        ).Provider()
        placeholders = (
            cnpj,
            name,
            description,
            email,
            phone,
            address,
        )
        self.entries = {}
        # padding at top
        tk.Label(self.gui, text="").grid(row=0, column=0, columnspan=2)

        # fields
        iterator = iter(fields)
        while True:
            try:
                field = next(iterator)
                index = fields.index(field)  # index of field
                # Name of field
                label = tk.Label(self.gui, text=field, width=20, anchor="w")
                label.grid(row=index + 1, column=0)
                # Entry of field
                self.entries[field] = ttk.Entry(self.gui, width=30)
                self.entries[field].grid(row=(index + 1), column=1, sticky=tk.W)
                self.entries[field].insert(0, placeholders[index])
                # Focus on first field
                if index == 0:
                    self.entries[field].focus()
            except StopIteration:
                break

        btn = ttk.Button(self.gui, text="Cadastrar", command=lambda: self.try_insert())
        btn.grid(row=len(fields) + 2, column=1, sticky=tk.W, pady=10)

        return

    def get_all_providers(self):
        provider = ProviderController(self.db).get_all_providers()
        if provider:
            TextOutput(self.root).display(provider, "Todos os fornecedor")
        else:
            messagebox.showinfo("Aviso", "não há fornecedores cadastrados")

    def get_provider_info(self):
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Obter informações do fornecedor")
        self.gui.geometry("300x100")
        CenterWindow(self.gui)

        tk.Label(self.gui, text="Escolha um dos fornecedores:").grid(row=0, column=0)
        self.provider = tk.StringVar(self.gui)

        display = lambda p: f"{p.get_id()} - {p.get_name()} - {p.get_cnpj()}"
        providers = ProviderController(self.db).get_all_providers()
        self.provider.set(display(providers[0]))
        op = tk.OptionMenu(self.gui, self.provider, *[display(p) for p in providers])
        op.config(width=20)
        op.grid(row=1, column=0, sticky=tk.W)
        btn = ttk.Button(
            self.gui, text="Mostrar", command=lambda: self._show_provider()
        )
        btn.grid(row=1, column=1, sticky=tk.W, pady=10)

    def _show_provider(self):
        provider_id = self.provider.get().split(" - ")[0]
        provider = ProviderController(self.db).get_provider_by_id(provider_id)
        if provider:
            TextOutput(self.root).display(str(provider), "Informações do fornecedor")
        else:
            messagebox.showinfo("Aviso", "não há fornecedores cadastrados")

    def try_insert(self):
        errors = self._validate_fields_provider()
        if show_errors(errors):
            return
        else:
            c = ProviderController(self.db)
            c.add_provider(
                Provider(
                    self.entries["CNPJ"].get(),
                    self.entries["Nome"].get(),
                    self.entries["Descrição"].get(),
                    self.entries["Email"].get(),
                    self.entries["Telefone"].get(),
                    self.entries["Endereço"].get(),
                )
            )
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso")
            self.gui.destroy()

    def _validate_fields_provider(self):
        errors = []
        cnpj = self.entries["CNPJ"].get()
        name = self.entries["Nome"].get()
        description = self.entries["Descrição"].get()
        email = self.entries["Email"].get()
        phone = self.entries["Telefone"].get()
        address = self.entries["Endereço"].get()

        # validar CNPJ
        if cnpj is None:
            errors.append("CNPJ não deve estar vazio")
        if len(cnpj) != 14:
            errors.append("CNPJ deve conter 14 digitos numéricos")
        iterator = iter(cnpj)
        while True:
            try:
                if not next(iterator).isdigit():
                    errors.append("CNPJ deve conter apenas números")
                    break
            except StopIteration:
                break

        # validar nome

        if name is None:
            errors.append("nome não deve estar vazio")
        if len(name) < 3 & len(name) > 50:
            errors.append(
                "Nome deve conter no mínimo 3 caracteres e no máximo 50 caracteres"
            )

        # validar descrição
        if description is None:
            errors.append("Descrição não pode estar vazia")
        if len(description) < 3:
            errors.append("Descrição deve conter no mínimo 3 caracteres")
        if len(description) > 500:
            errors.append("Descrição deve conter no máximo 500 caracteres")

        # validar email
        if email is None:
            errors.append("Email não pode estar vazio")
        if "@" not in email:
            errors.append("Email deve conter @")
        if "." not in email:
            errors.append("Email deve conter .")
        if email.count("@") > 1:
            errors.append("Email deve conter apenas um @")

        # validar telefone
        if phone is None:
            errors.append("Telefone não deve estar vazio")
        if len(phone) != 11:
            errors.append("Telefone deve conter onze digitos")
        while True:
            try:
                if not next(iterator).isdigit():
                    errors.append("Telefone deve conter apenas números")
                    break
            except StopIteration:
                break

        # validar enedereço
        if len(address) < 5:
            errors.append("Endereço deve conter no mínimo 5 caracteres")

        return errors


class SaleUI:
    def __init__(self, root: tk.Tk, db: str = "app.db"):
        self.root = root
        self.db = db

    def add_sale(self):
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Cadastro de Venda")
        self.gui.geometry("500x225")
        f_width = 25
        CenterWindow(self.gui)
        r = 0
        tk.Label(self.gui, text="").grid(row=r, column=0, columnspan=2)
        r += 1
        display = lambda p: f"{p.get_id()} - {p.get_name()} - {p.get_cpf()}"
        sellers = UserController(self.db).get_all_sellers()
        customers = UserController(self.db).get_all_customers()
        # Seller
        tk.Label(self.gui, text="Vendedor", width=25, anchor="w").grid(row=r, column=0)
        self.seller = tk.StringVar(self.gui)
        self.seller.set(display(sellers[0]))
        op_s = tk.OptionMenu(self.gui, self.seller, *[display(i) for i in sellers])
        op_s.config(width=f_width)
        op_s.grid(row=r, column=1)
        r += 1
        # Customer
        tk.Label(self.gui, text="Cliente", width=25, anchor="w").grid(row=r, column=0)
        self.customers = tk.StringVar(self.gui)
        self.customers.set(display(customers[0]))
        op_c = tk.OptionMenu(self.gui, self.customers, *[display(i) for i in customers])
        op_c.config(width=f_width)
        op_c.grid(row=r, column=1)
        r += 1
        # Date
        tk.Label(self.gui, text="Data", width=f_width, anchor="w").grid(row=r, column=0)
        self.date = tk.StringVar(self.gui)
        self.date.set(date.now().strftime("%Y-%m-%d"))
        tk.Entry(self.gui, text=self.date, width=25).grid(row=r, column=1)
        r += 1
        # Products
        tk.Label(self.gui, text="Produtos", width=f_width, anchor="w").grid(
            row=r, column=0
        )
        # Open a new window to select products
        self.products = []
        tk.Label(self.gui, text="Valor Bruto", width=f_width, anchor="w").grid(
            row=r + 1, column=0
        )
        self.price_label = tk.Label(self.gui, text="0", width=25)
        self.price_label.grid(row=r + 1, column=1)
        btn = ttk.Button(
            self.gui, text="Selecionar", command=lambda: self._select_products()
        )
        btn.grid(row=r, column=1, sticky=tk.W, pady=10)

        btn2 = ttk.Button(
            self.gui, text="Limpar", command=lambda: self._clear_products()
        )
        btn2.grid(row=r, column=1, sticky=tk.W, pady=10, padx=100)
        r += 2

        # Buttons
        btn = ttk.Button(
            self.gui, text="Cadastrar", command=lambda: self._insert_sale()
        )
        btn.grid(row=r, column=1, sticky=tk.W, pady=10, padx=20)
        btn2 = ttk.Button(self.gui, text="Cancelar", command=lambda: self.gui.destroy())
        btn2.grid(row=r, column=0, sticky=tk.E, pady=10, padx=20)

    def _insert_sale(self):
        # Count equal products
        products: list[Product] = self.products
        count = {}
        iterator = iter(products)
        while True:
            try:
                pid = next(iterator).get_id()
                if pid in count:
                    count[pid] += 1
                else:
                    count[pid] = 1
            except StopIteration:
                break

        # Create SaleItem
        self.sale_items = []
        iterator = iter(count)
        while True:
            try:
                i = next(iterator)
                product = ProductController(self.db).get_product_by_id(i)
                quantity = count[i]
                self.sale_items.append(SaleItem(product, quantity))
            except StopIteration:
                break

        # Create Sale
        customer_id = self.customers.get().split(" - ")[0]
        customer = UserController(self.db).get_customer_by_id(customer_id)
        seller_id = self.seller.get().split(" - ")[0]
        seller = UserController(self.db).get_seller_by_id(seller_id)
        self.sale = None
        try:
            sale_date = date.strptime(self.date.get(), "%Y-%m-%d")
            self.sale: Sale = Sale(
                customer=customer,
                seller=seller,
                date=sale_date,
                itens=self.sale_items,
                payment_method=None,
            )
            self._select_payment()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida")

    def _update_price(self):
        self.price_label.config(
            text=f"{round(sum([i.get_price() for i in self.products]), 2)}"
        )

    def _clear_products(self):
        self.products = []
        self._update_price()

    def _select_products(self):
        self.gui_p = tk.Toplevel(self.root)
        self.gui_p.title("Selecionar produtos")
        self.gui_p.geometry("400x100")
        CenterWindow(self.gui_p)
        self.gui_p.grab_set()
        self.gui_p.focus_set()
        r = 0
        tk.Label(self.gui_p, text="").grid(row=r, column=0, columnspan=2)
        r += 1
        display = lambda p: f"{p.get_id()} - {p.get_name()} - {p.get_price()}"
        products = ProductController(self.db).get_all_products()
        self.product = tk.StringVar(self.gui_p)
        self.product.set(display(products[0]))
        op = tk.OptionMenu(self.gui_p, self.product, *[display(i) for i in products])
        op.config(width=25)
        op.grid(row=r, column=0, sticky=tk.W)
        # Field that only accepts numbers
        self.quantity = tk.StringVar(self.gui_p)
        self.quantity.set("1")
        tk.Entry(self.gui_p, text=self.quantity, width=5).grid(row=r, column=1)
        btn = ttk.Button(
            self.gui_p,
            text="Adicionar",
            command=lambda: self._add_product_to_cart(),
        )
        btn.grid(row=r, column=2, sticky=tk.W, pady=10)

    def _add_product_to_cart(self):
        product_id = self.product.get().split(" - ")[0]
        quantity = 1
        try:
            quantity = int(self.quantity.get())
            selected = ProductController(self.db).get_product_by_id(product_id)
            iterator = iter(range(quantity))
            while True:
                try:
                    next(iterator)
                    self.products.append(selected)
                except StopIteration:
                    break
            self._update_price()
        except ValueError:
            messagebox.showinfo("Erro", "Quantidade inválida")

    def get_all_sales(self):
        sale = SaleController(self.db).get_all_sales()
        if sale:
            TextOutput(self.root).display(sale, "Vendas realizadas")
        else:
            messagebox.showinfo("Aviso", "não existem vendas cadastradas")

    def get_sale_info(self):
        self.gui: tk.Toplevel = tk.Toplevel(self.root)
        self.gui.title("Obter informações das vendas")
        self.gui.geometry("350x170")
        CenterWindow(self.gui)
        tk.Label(self.gui, text="Selecione a venda desejada:").pack(pady=10)
        sales = SaleController(self.db).get_all_sales()
        if sales:

            def display(sale: Sale):
                return f"{sale.get_id()} - Realizada em {str(sale.get_date())[:10]} por {sale.get_customer().get_name()} no valor de R${round(sale.calculate_total_value(), 2)}"

            self.sale = tk.StringVar(self.gui)
            self.sale.set(display(sales[0]))
            op = tk.OptionMenu(self.gui, self.sale, *[display(i) for i in sales])
            op.config(width=25)
            op.pack(pady=10)
            btn = ttk.Button(
                self.gui,
                text="Obter informações",
                command=lambda: TextOutput(self.gui).display(
                    str(
                        SaleController(self.db).get_sale_by_id(
                            self.sale.get().split(" - ")[0]
                        )
                    )
                ),
            )
            btn.pack(pady=10)
        else:
            messagebox.showinfo("Aviso", "Não existem vendas cadastradas")

    def _show_sale(self):
        sale_id = self.sale.get().split(" - ")[0]
        sale = SaleController(self.db).get_sale_by_id(sale_id)
        if sale:
            TextOutput(self.root).display(str(sale), "Informações da venda")
        else:
            messagebox.showinfo("Aviso", "Esta venda não existe")

    def get_monthly_sales(self):
        self.gui: tk.Toplevel = tk.Toplevel(self.root)
        self.gui.title("Obter vendas de um mês especifico")
        self.gui.geometry("350x170")
        CenterWindow(self.gui)
        tk.Label(self.gui, text="Selecione a data da venda desejada: (AAAA-MM)").pack(
            pady=10
        )
        self.month = tk.Entry(self.gui, width=30)
        self.month.pack()
        self.month.insert(0, date.today().strftime("%Y-%m"))

        def _parse_date(datetime: str, format: str) -> date:
            try:
                return date.strptime(datetime, format)
            except ValueError:
                messagebox.showerror("Erro", "Data inválida")

        def _show(sale):
            if sale:
                sales, total = sale
                string = f"Vendas do mês {self.month.get()}:\n"
                iterator = iter(sales)
                while True:
                    try:
                        string += str(next(iterator)) + "\n"
                    except StopIteration:
                        break
                string += f"\n\nTotal: R${round(total, 2)}"
                TextOutput(self.root).display(
                    string, f"Vendas do mês {self.month.get()}"
                )
            else:
                messagebox.showinfo("Aviso", "Não existem vendas neste período")

        def _show_sales():
            mm, yy, = (
                self.month.get(),
                self.month.get(),
            )
            _show(
                SaleController(self.db).get_all_sales_in_month(
                    str(_parse_date(mm, "%Y-%m").month),
                    str(_parse_date(yy, "%Y-%m").year),
                )
            )

        button = tk.Button(
            self.gui,
            text="Obter vendas do mês",
            command=_show_sales,
        )
        button.pack(pady=10)

    def get_all_sales_paid_via_cash(self):
        sale = SaleController(self.db).get_all_sales_paid_via_cash()
        if sale:
            TextOutput(self.root).display(
                sale, "Todas as vendas realizadas com dinheiro"
            )
        else:
            messagebox.showinfo(
                "Aviso", "Não foram realizadas vendas pagas em dinheiro"
            )

    def get_all_sales_paid_via_card(self):
        sale = SaleController(self.db).get_all_sales_paid_via_card()
        if sale:
            TextOutput(self.root).display(sale, "Todas as vendas realizadas com cartão")
        else:
            messagebox.showinfo("Aviso", "Não foram realizadas vendas pagas via cartão")

    def get_all_sales_paid_via_pix(self):
        sale = SaleController(self.db).get_all_sales_paid_via_pix()
        if sale:
            TextOutput(self.root).display(sale, "Todas as vendas realizadas com pix")
        else:
            messagebox.showinfo("Aviso", "Não foram realizadas vendas com Pix")

    def get_customer_history(self):
        self.gui = tk.Toplevel(self.root)
        self.gui.title("Obter histórico de compras")
        self.gui.geometry("350x170")
        CenterWindow(self.gui)
        tk.Label(self.gui, text="Selecione o cliente desejado:").pack(pady=10)
        customers = UserController(self.db).get_all_customers()
        if customers:

            def display(customer: Customer):
                return f"{customer.get_id()} - {customer.get_name()}"

            self.customer = tk.StringVar(self.gui)
            self.customer.set(display(customers[0]))
            op = tk.OptionMenu(
                self.gui, self.customer, *[display(i) for i in customers]
            )
            op.config(width=25)
            op.pack(pady=10)
            btn = ttk.Button(
                self.gui,
                text="Obter histórico",
                command=lambda: TextOutput(self.gui).display(
                    SaleController(self.db).get_customer_history(
                        self.customer.get().split(" - ")[0]
                    ),
                    f"Histórico do cliente {self.customer.get().split(' - ')[1]}",
                ),
            )
            btn.pack(pady=10)

    def _select_payment(self):
        self.gui_payment = tk.Toplevel(self.root)
        self.gui_payment.title("Método de Pagamento")
        self.gui_payment.geometry("245x200")
        CenterWindow(self.gui_payment)
        r = 0
        tk.Label(self.gui_payment, text="").grid(row=r, column=0, columnspan=2)
        r += 1
        tk.Label(self.gui_payment, text="Selecione o método de pagamento:").grid(
            row=r, column=0, columnspan=2
        )
        r += 1

        self.payment = tk.StringVar(self.gui_payment)
        self.payment.set("Dinheiro")
        op = tk.OptionMenu(
            self.gui_payment, self.payment, "Dinheiro", "Cartão de Crédito", "Pix"
        )
        op.config(width=25)
        op.grid(row=r, column=0, sticky=tk.W)
        r += 1

        brute_price = round(float(self.price_label.cget("text")), 2)
        tk.Label(self.gui_payment, text=f"Valor Bruto: {brute_price}").grid(
            row=r, column=0, sticky=tk.W
        )
        r += 1

        tk.Label(
            self.gui_payment,
            text=f"Desconto (Cliente Ouro): {round(self.sale.get_discount(), 2)}",
        ).grid(row=r, column=0, sticky=tk.W)
        r += 1

        tk.Label(
            self.gui_payment,
            text=f"Impostos: {round(self.sale.get_taxes(), 2)}",
        ).grid(row=r, column=0, sticky=tk.W)
        r += 1

        self.total_value = self.sale.calculate_total_value()
        self.value = tk.Label(
            self.gui_payment, text="Valor total: " + str(round(self.total_value, 2))
        )
        self.value.grid(row=r, column=0, sticky=tk.W)
        r += 1

        ttk.Button(
            self.gui_payment,
            text="Pagar",
            command=lambda: self._pay_sale(),
        ).grid(row=r, column=0, sticky=tk.W, pady=10, padx=75)

    def _pay_sale(self):
        if self.payment.get() == "Dinheiro":
            self.type = "cash"
            self._try_insert()
        elif self.payment.get() == "Cartão de Crédito":
            self._card_info_UI()
        elif self.payment.get() == "Pix":
            self._pix_info_UI()

    def _card_info_UI(self):
        self.type = "card"
        self.gui_card = tk.Toplevel(self.root)
        self.gui_card.title("Informações do Cartão")
        self.gui_card.geometry("450x200")
        CenterWindow(self.gui_card)
        [_, name, flag, number] = RandomObjectInfo(
            self.db, self.db, self.db
        ).Credit_card_payment(self.sale.get_customer().get_name())
        r = 0
        tk.Label(self.gui_card, text="").grid(row=r, column=0, columnspan=2)
        r += 1
        tk.Label(self.gui_card, text="Informações do cartão").grid(
            row=r, column=0, columnspan=2
        )
        r += 1
        tk.Label(self.gui_card, text="Nome do titular:").grid(
            row=r, column=0, sticky=tk.W
        )
        self.card_holder = tk.Entry(self.gui_card, width=25)
        self.card_holder.grid(row=r, column=1, sticky=tk.W)
        self.card_holder.insert(0, name)
        r += 1
        tk.Label(self.gui_card, text="Número do cartão:").grid(
            row=r, column=0, sticky=tk.W
        )
        self.card_number = tk.Entry(self.gui_card, width=25)
        self.card_number.insert(0, number)
        self.card_number.grid(row=r, column=1, sticky=tk.W)
        r += 1
        tk.Label(self.gui_card, text="Bandeira:").grid(row=r, column=0, sticky=tk.W)
        self.card_flag = tk.Entry(self.gui_card, width=25)
        self.card_flag.grid(row=r, column=1, sticky=tk.W)
        self.card_flag.insert(0, flag)
        r += 1
        btn = ttk.Button(
            self.gui_card,
            text="Pagar",
            command=lambda: self._try_insert(),
        )
        btn.grid(row=r, column=0, sticky=tk.W, pady=10, padx=75)

    def _pix_info_UI(self):
        self.type = "pix"
        self.gui_pix = tk.Toplevel(self.root)
        self.gui_pix.title("Código Pix")
        self.gui_pix.geometry("400x150")
        CenterWindow(self.gui_pix)
        [_, code] = RandomObjectInfo(self.db, self.db, self.db).Pix_payment()
        r = 0
        tk.Label(self.gui_pix, text="Código Pix (32 caracteres)").pack(pady=10)
        r += 1
        self.pix_code = tk.Entry(self.gui_pix, width=25)
        self.pix_code.pack(pady=10)
        # self.pix_code.grid(row=r, column=1, sticky=tk.W)
        self.pix_code.insert(0, code)
        r += 1
        btn = ttk.Button(
            self.gui_pix,
            text="Pagar",
            command=lambda: self._try_insert(),
        )
        btn.pack(pady=10)

    def _try_insert(self):
        errors = self._validate_payment_entries()
        if show_errors(errors):
            return
        else:
            c = SaleController(self.db)
            payment = None
            if self.type == "card":
                payment = CreditCard(
                    "Cartão",
                    self.card_holder.get(),
                    self.card_flag.get(),
                    self.card_number.get(),
                )
            elif self.type == "pix":
                payment = Pix("Pix", self.pix_code.get())
            elif self.type == "cash":
                payment = Cash("Dinheiro")
            else:
                raise Exception("Tipo de pagamento não definido")
            p_id = c.insert_payment(payment)
            payment.set_id(p_id)
            self.sale.set_payment_method(payment)
            c.insert_sale(self.sale)
            messagebox.showinfo("Aviso", "Venda realizada com sucesso")
            self.gui.destroy()
            self.gui_payment.destroy()

    def _validate_payment_entries(self):
        errors = []
        if self.type == "card":
            if not self.card_holder.get():
                errors.append("Nome do titular não preenchido")
            if not self.card_number.get():
                errors.append("Número do cartão não preenchido")
            if not self.card_flag.get():
                errors.append("Bandeira do cartão não preenchido")
            return errors
        elif self.type == "pix":
            if not self.pix_code.get():
                errors.append("Código Pix não preenchido")
            if len(self.pix_code.get()) != 32:
                errors.append("Código Pix deve ter 32 caracteres")
        return errors
