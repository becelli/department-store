import random as random
from datetime import datetime as date
from xmlrpc.client import Boolean
from controller.provider import ProviderController

from model.classes.product import Clothing, Electronic, Food, Home_Appliance, Product
from model.classes.payment import Pix, Cash, CreditCard
from model.classes.provider import Provider
from model.classes.user import Customer, Seller
from model.classes.sale import Sale


class RandomObjectInfo:
    def __init__(
        self,
        product_db: str = "app.db",
        user_db: str = "app.db",
        provider_db: str = "app.db",
    ):
        self._product_db_name = product_db
        self._user_db_name = user_db
        self._provider_db_name = provider_db

    def Electronic(self) -> list:
        current_year = date.now().year
        name = self._random_electronic_device()
        description = f"{name} {self._random_electronics_description()}"
        fabrication = random.randint(current_year - 7, current_year)
        price = round(random.randint(100, 1000) + random.random(), 2)
        provider = ProviderController(self._provider_db_name).get_random_provider()
        is_available = True
        return name, description, fabrication, price, provider, is_available

    def Home_Appliance(self) -> list:
        current_year = date.now().year
        name = self._random_home_devices_names()
        description = f"{name} {self._random_homeappliance_description()}"
        fabrication = random.randint(current_year - 10, current_year)
        price = round(random.randint(1000, 10000), 2)
        provider = ProviderController(self._provider_db_name).get_random_provider()
        is_available = True
        return name, description, fabrication, price, provider, is_available

    def Food(self) -> list:
        current_year = date.now().year
        name = self._random_food_name()
        description = f"{name} {self._random_product_description()}"
        provider = ProviderController(self._provider_db_name).get_random_provider()
        fabrication = random.randint(current_year - 1, current_year)
        price = round(random.randint(10, 200), 2)
        is_available = True
        return name, description, fabrication, price, provider, is_available

    def Clothing(self) -> list:
        current_year = date.now().year
        name = self._random_clothing_name()
        description = f"{name} {self._random_clothing_description()}"
        fabrication = random.randint(current_year - 8, current_year)
        price = round(random.randint(30, 500), 2)
        provider = ProviderController(self._provider_db_name).get_random_provider()
        is_available = True
        return name, description, fabrication, price, provider, is_available

    def Customer(self) -> list:
        name = self._names()
        cpf = self._nsize_num_as_str(11)  # rg
        rg = self._nsize_num_as_str(9)  # cpf
        date = self._date()
        address = self._random_street_name()
        zip_code = f"{self._nsize_num_as_str(5)}-{self._nsize_num_as_str(3)}"
        email = (
            name.split(" ")[0].lower() + (self._nsize_num_as_str(5)) + self._emails()
        )
        golden = self._bool_rand()
        return name, cpf, rg, date, address, zip_code, email, golden

    def Seller(self) -> list:
        name = self._names()
        rg = self._nsize_num_as_str(11)  # cpfpc.get_random_provider()
        cpf = self._nsize_num_as_str(9)  # rg
        bdate = self._date()
        address = self._random_street_name()
        zip_code = f"{self._nsize_num_as_str(5)}-{self._nsize_num_as_str(3)}"
        email = (
            name.split(" ")[0].lower() + (self._nsize_num_as_str(5)) + self._emails()
        )
        salary = round(random.randint(1000, 5000), 2)
        pis = self._nsize_num_as_str(11)
        admission = self._date(bdate.year + 16, date.now().year)
        return name, rg, cpf, bdate, address, zip_code, email, salary, pis, admission

    def Provider(self) -> list:
        cnpj = (
            self._nsize_num_as_str(8)
            + f"000{random.randint(1, 9)}"
            + self._nsize_num_as_str(2)
        )
        r = random.randint(0, 2)
        extra = "" if r == 0 else " LTDA" if r == 1 else " MEI"
        name = self._provider_name() + extra
        description = self._provider_description()
        email = name.split(" ")[0].lower() + self._nsize_num_as_str(3) + self._emails()
        phone = self._nsize_num_as_str(11)
        address = self._random_street_name()
        return cnpj, name, description, email, phone, address

    def Cash_payment(self) -> list[str]:
        return "Dinheiro"

    def Credit_card_payment(self, name: str = None) -> list[str, str, str, str]:
        payment_type = "Cartão"
        name = name if name else self._names()
        flag = self._card_flag()
        number = self._nsize_num_as_str(16)
        return payment_type, name, flag, number

    def Pix_payment(self) -> list[str, str]:
        payment_type = "Pix"
        code = self._nsize_num_as_str(32)
        return payment_type, code

    def Sale(self):
        from controller.user import UserController

        uc = UserController(self._user_db_name)
        customer = uc.select_random_customer()
        seller = uc.select_random_seller()
        sale_date = self._date()
        payment_code = random.randint(1, 3)
        if payment_code == 1:
            payment_method = self.Cash_payment()
        elif payment_code == 2:
            payment_method = self.Credit_card_payment()
        elif payment_code == 3:
            payment_method = self.Pix_payment()

        return customer, seller, sale_date, payment_method

    def Sale_item(self) -> list[Product, int]:
        import controller.product as pdc

        products = pdc.Product(self._product_db_name).select_all_products()
        product: Product = random.choice(products)
        quantity = random.randint(1, 10)
        return product, quantity

    def _random_credit_card_name(self) -> str:
        credit_cards = [
            "Pan",
            "Master Card",
            "Next Visa",
            "Original Internacional",
            "Nubank",
            "Gold card",
            "Platinium card",
            "Diamond card",
            "New visa",
            "card",
            "Digio",
            "Inter plus",
        ]
        return random.choice(credit_cards)

    def _random_clothing_name(self):
        clothes = [
            "Calça",
            "Blusa",
            "Camisa",
            "Sapato",
            "Chinelo",
            "Sapatenis",
            "Chuteira",
            "Crock",
            "Sandália",
            "Meias",
            "Blusa Jeans",
            "Short",
            "Short Jeans",
            "Camiseta",
            "Blusa com capuz",
        ]
        return random.choice(clothes)

    def _random_clothing_description(self):
        clothing_description = [
            "da Nike",
            "azul",
            "vermelho",
            "rosa",
            "preto",
            "verde",
            "roxo",
            "verde claro",
            "verde escuro",
            "amarelo",
            "premium",
            "premium +",
            "listrado",
            "branco",
            "com revestimento",
            "marrom",
            "lilás",
            "vermelho vinho",
            "azul escuro",
            "azul claro",
            "ciano",
            "cor gradiente",
        ]
        return random.choice(clothing_description)

    def _random_food_name(self):
        foods = [
            "Hamburguer",
            "Pizza",
            "Sushi",
            "Sorvete",
            "Coxinha",
            "Macarrão",
            "Pão de Queijo",
            "Estrogonofe",
            "Pudim",
            "Pizza",
            "Salada",
            "Batata Frita",
            "Café",
            "Chocolate",
            "Suco",
            "Refrigerante",
            "Cerveja",
            "Cereja",
        ]
        return random.choice(foods)

    def _random_product_description(self):
        description_product = [
            "da casa",
            "gourmet",
            "de Minas",
            "nordestino",
            "do Pará",
            "santista",
            "paulista",
            "carioca",
            "a la carte",
        ]
        return random.choice(description_product)

    def _random_home_devices_names(self):
        home_devices = [
            "Fogão",
            "Geladeira",
            "Microondas",
            "Máquina de Lavar",
            "Ventilador",
            "Rádio",
            "Secadora",
            "Secador de Cabelo",
            "Ar condicionado",
            "Frigobar",
        ]
        return random.choice(home_devices)

    def _random_homeappliance_description(self):
        home_devices_descriptions = [
            "qualidade comprovada pelo INMETRO",
            "melhor produto da região",
            "tecnologia de ponta",
            "Made in China",
            "Melhor eficiência do mercado",
            "Premium",
            "Prateado",
            "Dourado",
        ]
        return random.choice(home_devices_descriptions)

    def _random_electronics_description(self):
        description = [
            "Xiaomi",
            "Samsung",
            "Apple",
            "LG",
            "Sony",
            "Philips",
            "Panasonic",
        ]
        return random.choice(description)

    def _random_electronic_device(self):
        devices = [
            "Smartphone",
            "Tablet",
            "Notebook",
            "Rádio",
            "Smart TV",
            "Smart Watch",
            "Lâmpada Inteligente",
            "Smart Speaker",
        ]
        return random.choice(devices)

    def _provider_name(self):
        providers = [
            "Sublime",
            "Alfa Seven",
            "Porto Alegre",
            "Emerald Products",
            "Queensberry",
            "Gini",
            "Premium Stocks",
            "Wilson",
            "Chelkem",
            "Trio Armazém",
            "APTI",
            "Royal Pack",
            "Ryu Supplies",
            "Premier",
            "Premier Plus",
            "Bela Vista",
            "Royal Production",
            "Old Joey Stocks",
        ]
        return random.choice(providers)

    def _random_street_name(self):
        streets = [
            "Irlanda",
            "25 de abril",
            "Tira dentes",
            "Cássio",
            "Bashirian Falls",
            "Fabiola Mount",
            "Florencio Fields",
            "Green Coves",
            "Addie Corners",
            "Shields Roads",
            "Abner Parkways",
            "Macejkovic Isle",
            "Gregorio Key",
            "Tyra Courts",
            "Kiara Loop",
        ]
        return f"Rua {random.choice(streets)}"

    def _bool_rand(self):
        return random.choice([True, False])

    def _card_flag(self) -> str:
        flags = ["Visa", "Mastercard", "American Express", "Hipercard", "Elo"]
        return random.choice(flags)

    def _emails(self):
        emails = [
            "@gmail.com",
            "@hotmail.com",
            "@hao123.com",
            "@outlook.com",
            "@msn.com",
            "@baidu.com",
            "@live.com",
            "@yahoo.com",
            "@qq.com",
        ]
        return random.choice(emails)

    def _provider_description(self):
        providers_description = [
            "10 anos no serviço",
            "15 anos no serviço",
            "20 anos no serviço",
            "melhores produtos no mercado",
            "melhor fornecedor da região",
            "produtos tradicionais",
            "com tecnologia de ponta",
            "melhores profissionais",
            "produtos com selo de garantia",
            "aprovado pelo inmetro",
            "produtos premium",
        ]

        return random.choice(providers_description)

    # Generate random date as a string.

    def _date(self, y_min: int = 1950, y_max: int = 2003):
        dt = self._date_as_string(y_min, y_max)
        return date.strptime(dt, "%Y-%m-%d")

    def _date_as_string(self, y_min: int = 1950, y_max: int = 2003):
        birth_day = self._nsize_padded_num_as_str(2, 1, 28)
        birth_month = self._nsize_padded_num_as_str(2, 1, 12)
        birth_year = self._nsize_padded_num_as_str(4, y_min, y_max)
        birth_date = f"{birth_year}-{birth_month}-{birth_day}"
        return birth_date

    # Generate random letter.

    def _nsize_padded_num_as_str(
        self, size: int, min_value: int = 0, max_value: int = 9
    ):
        num = random.randint(min_value, max_value)
        num = str(num)
        for _i in range(size - len(num)):
            num = "0" + num
        return num

    # Generate random number with a fixed size. It may contain zeros at the beginning.
    def _nsize_num_as_str(self, size: int, min_value: int = 0, max_value: int = 9):
        num = ""
        for _i in range(size):
            num += str(random.randint(min_value, max_value))
        return num

    def _names(self) -> str:
        firstnames = [
            "Clara",
            "Wesley",
            "Gustavo",
            "João",
            "Maria",
            "José",
            "Pedro",
            "Paulo",
            "Lucas",
            "Joana",
            "Roberto",
            "Vinicius",
            "Mariana",
            "Ana",
            "Paula",
            "Larissa",
            "Marcos",
            "Joaquim",
            "Rafael",
            "Ricardo",
            "Fernando",
            "Luiz",
            "Eduardo",
            "Henrique",
            "Vitor",
            "Gabriel",
            "Clarisse",
            "Rafaela",
            "Leticia",
            "Bruno",
            "Roberta",
            "Daniel",
            "Emanuel",
            "Gabriela",
            "Eduarda",
            "Eva",
            "Adão",
            "Ana Paula",
            "Antônio",
            "Benedito",
            "Bianca",
            "Bruna",
            "Catarina",
            "Cecília",
            "Cristiane",
            "Davi",
            "Samuel",
            "Sophia",
            "Thiago",
            "Vitória",
            "Cleiton",
            "Cleverson",
            "Wagner",
            "Waldir",
            "Xavier",
            "Yuri",
            "Sérgio",
            "Sônia",
            "Fábio",
            "Fátima",
            "Fernando",
            "Fernanda",
            "Débora",
            "Décio",
            "Solange",
            "Sabrina",
            "Cristian",
            "Calisto",
        ]
        lastnames = [
            "Silva",
            "Santos",
            "Oliveira",
            "Pereira",
            "Souza",
            "Costa",
            "Rodrigues",
            "Almeida",
            "Martins",
            "Araújo",
            "Simolini",
            "Becelli",
            "Borges",
            "Bruno",
            "Cabral",
            "Carvalho",
            "Cardoso",
            "Cunha",
            "Dias",
            "Domingues",
            "Fernandes",
            "Fernando",
            "Gomes",
            "Gonçalves",
            "Henrique",
            "Jesus",
            "Lima",
            "Lopes",
            "Macedo",
            "Moraes",
            "Moreira",
            "Moura",
            "Nascimento",
            "Nogueira",
            "Oliveira",
            "Pacheco",
            "Pereira",
            "Ramos",
            "Ribeiro",
            "Rocha",
            "Serra",
            "Teixeira",
            "Vieira",
            "Valente",
            "Voss",
            "Xavier",
            "Zanella",
            "Zanetti",
            "Zanin",
            "Zanoni",
            "Umbelino",
            "Umbelita",
            "Quaresma",
            "Queiroz",
            "Ernesto",
            "Bernardes",
            "Bianchi",
            "Bianco",
            "Brunelli",
            "Durante",
            "Duccio",
            "Duchini",
        ]
        return f"{random.choice(firstnames)} {random.choice(lastnames)}"


class RandomObject:
    def __init__(
        self,
        product_db: str = "app.db",
        user_db: str = "app.db",
        provider_db: str = "app.db",
    ):
        self._product_db_name = product_db
        self._user_db_name = user_db
        self._provider_db_name = provider_db
        self.data_source: RandomObjectInfo = RandomObjectInfo(
            product_db, user_db, provider_db
        )

    def Customer(self):
        c = self.data_source.Customer()
        return Customer(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])

    def Seller(self):
        s = self.data_source.Seller()
        return Seller(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9])

    def Provider(self):
        p = self.data_source.Provider()
        return Provider(p[0], p[1], p[2], p[3], p[4], p[5])

    def Sale(self):
        sl = self.data_source.Sale()
        return Sale(sl[0], sl[1], sl[2], sl[3])

    def Payment(self):
        r = random.randint(0, 2)
        if r == 0:
            return self.Cash()
        if r == 1:
            return self.Credit_card()
        if r == 2:
            return self.Pix()

    def Cash(self):
        cs = self.data_source.Cash_payment()
        return Cash(cs[0])

    def Credit_card(self):
        cc = self.data_source.Credit_card_payment()
        return CreditCard(cc[0], cc[1], cc[2], cc[4])

    def Pix(self):
        px = self.data_source.Pix_payment()
        return Pix(px[0], px[1])

    def Product(self):
        r = random.randint(0, 3)
        if r == 0:
            return self.Electronic()
        if r == 1:
            return self.Food()
        if r == 2:
            return self.Clothing()
        if r == 3:
            return self.Home_appliance()

    def Electronic(self):
        # return name, description, fabrication, price, provider, is_available
        el = self.data_source.Electronic()
        return Electronic(el[0], el[1], el[2], el[3], el[4], el[5])

    def Food(self):
        el = self.data_source.Food()
        return Food(el[0], el[1], el[2], el[3], el[4], el[5])

    def Home_appliance(self):
        el = self.data_source.Home_Appliance()
        return Home_Appliance(el[0], el[1], el[2], el[3], el[4], el[5])

    def Clothing(self):
        el = self.data_source.Clothing()
        return Clothing(el[0], el[1], el[2], el[3], el[4], el[5])
