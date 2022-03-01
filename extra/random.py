import random as random
from model.classes import (
    payment as p,
    product as pd,
    provider as pr,
    sale as s,
    user as u,
)
from datetime import datetime as date


class RandomObjectInfo:
    def __init__(self, product_db: str = "app.db", user_db: str = "app.db"):
        self._product_db_name = product_db
        self._user_db_name = user_db

    def Electronic(self) -> list:
        current_year = date.now().year
        device_name = self._random_electronic_device()
        device_description = device_name + " " + self._ramdom_eletronics_description()
        fabrication_year = random.randint(current_year - 7, current_year)
        price = random.randint(100, 1000) + random.random()
        provider = self._provider_name()
        is_available = True
        return [
            device_name,
            device_description,
            fabrication_year,
            price,
            provider,
            is_available,
        ]

    def HomeAppliance(self) -> pd.HomeAppliance:
        current_year = date.now().year
        name_home_apliances = self._random_home_devices_names()
        description_home_apliances = (
            name_home_apliances + "" + self._random_home_devices_descriptions()
        )
        fabrication_year_home_apliances = random.randint(
            current_year - 10, current_year
        )
        price_home_apliances = random.randint(1000, 10000)
        provider_home_apliances = (
            self._provider_name()
        )  # TODO implementar select providers
        is_avaliable_home_apliances = True
        return [
            name_home_apliances,
            description_home_apliances,
            fabrication_year_home_apliances,
            price_home_apliances,
            provider_home_apliances,
            is_avaliable_home_apliances,
        ]

    def Food(self) -> list:
        current_year = date.now().year
        food_name = self._random_food_name()
        food_description = food_name + "" + self._random_product_description()
        food_provider = self._provider_name()
        food_fabrication = random.randint(current_year - 1, current_year)
        food_price = random.radint(50, 200)
        food_is_avaliable = True
        return [
            food_name,
            food_description,
            food_fabrication,
            food_price,
            food_provider,
            food_is_avaliable,
        ]

    def Clothing(self) -> list:
        current_year = date.now().year
        clothing_name = self._random_clothes_names()
        clothing_description = clothing_name + "" + self._random_clothing_description()
        clothing_fabrication = random.randint(current_year - 8, current_year)
        clothing_price = random.randint(100 - 5000)
        clothing_provider = self._provider_name()
        clothing_is_avaliable = True
        return [
            clothing_name,
            clothing_description,
            clothing_fabrication,
            clothing_price,
            clothing_provider,
            clothing_is_avaliable,
        ]

    def Customer(self) -> list:
        customer_name = self._names()
        rg = self._nsize_num_as_str(11)  # cpf
        cpf = self._nsize_num_as_str(9)  # rg
        date = self._date()
        adress = self._random_street_name()
        zip_code = self._nsize_num_as_str(5)
        email = customer_name + (self._nsize_num_as_str(4)) + self._emails()
        ouro = self._bool_rand()
        return [
            customer_name,
            rg,
            cpf,
            date,
            adress,
            zip_code,
            email,
            ouro,
        ]

    def Seller(self) -> list:
        seller_name = (self._names(),)
        rg = self._nsize_num_as_str(11)  # cpf
        cpf = self._nsize_num_as_str(9)  # rg
        date = self._date()
        adress = self._random_street_name()
        zip_code = self._nsize_num_as_str(5)
        email = seller_name + (self._nsize_num_as_str(4)) + self._emails()
        salary = random.randint(1000 - 4000)
        pis = self._nsize_num_as_str(5)
        admission_date = self._date()
        return [
            seller_name,
            rg,
            cpf,
            date,
            adress,
            zip_code,
            email,
            salary,
            pis,
            admission_date,
        ]

    def Provider(self) -> list:
        cnpj = self._nsize_num_as_str(14)
        name = self._provider_name()
        description = self._provider_description()
        email = name + self._nsize_num_as_str(2) + self._emails()
        telefone = self._nsize_num_as_str(9)
        address = self._random_street_name()

        return [
            cnpj,
            name,
            description,
            email,
            telefone,
            address,
        ]

    def Cash_payment(self) -> list[str]:
        return "Dinheiro"

    def Credit_card_payment(self) -> list[str, str, str, str]:
        payment_type = "Cartão de credito"
        name = self._random_credit_card_names()
        flag = self._card_flag()
        number = self._nsize_num_as_str(16)
        return [
            payment_type,
            name,
            flag,
            number,
        ]

    def Pix_payment(self) -> list[str, str]:
        payment_type = "Pix"
        code = self._nsize_num_as_str(32)
        return [
            payment_type,
            code,
        ]

    def Sale(self):
        import controller.user as uc
        import controller.sale as sc
        import controller.product as pdc

        customer = uc.UserController(self._user_db_name).select_random_customer()
        seller = uc.UserController(self._user_db_name).select_random_seller()
        sale_date = self._date()
        payment_code = random.randint(1, 3)
        if payment_code == 1:
            payment_method = self.Cash_payment()
        elif payment_code == 2:
            payment_method = self.Credit_card_payment()
        elif payment_code == 3:
            payment_method = self.Pix_payment()

        return [
            customer,
            seller,
            sale_date,
            payment_method,
        ]

    def Sale_item(self) -> list[pd.Product, int]:
        import controller.product as pdc

        products = pdc.Product(self._product_db_name).select_all_products()
        product: pd.Product = random.choice(products)
        quantity = random.randint(1, 10)
        return [product, quantity]

    #
    #
    #
    # atributos gerais
    #
    #
    #
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
        return [random.choice(credit_cards)]

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
            "Sandalha",
            "Meias",
            "Blusa Jeans",
            "Short",
            "Short Jeans",
            "Camiseta",
            "Blusa com capuz",
        ]
        return [random.choice(clothes)]

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
        return [random.choice(clothing_description)]

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
        return [random.choice(foods)]

    def _random_product_description(self):
        description_product = [
            "da casa",
            "de ouro",
            "gourmet",
            "de Minas",
            "nordestino",
            "do Pará",
            "santista",
            "paulista",
            "carioca",
            "a la carte",
        ]
        return [random.choice(description_product)]

    def _random_home_devices_names(self):
        home_devices = [
            "Fogão",
            "Geladeira",
            "Microondas",
            "Máquina de Lavar",
            "Ventilador",
            "Televisão",
            "Computador",
            "Notebook",
            "Rádio",
        ]
        return [random.choice(home_devices)]

    def _random_home_devices_descriptions(self):
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

    def _ramdom_eletronics_description(self):
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
        return ["Rua" + "" + random.choice(streets)]

    def _bool_rand(self):
        rad = random.randint(1, 2)
        if rad == 1:
            return True
        return [False]

    def _card_flag(self) -> str:
        flags = ["Visa", "Mastercard", "American Express", "Hipercard", "Elo"]
        return random.choice(flags)

    def _emails(self):
        emails = [
            "@gmail.com",
            "@htomail.com",
            "@hao123.com",
            "@outlook.com",
            "@msn.com",
            "@baidu.com",
            "@microsoft.com",
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

    def _date(self):
        dt = self._date_as_string()
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
