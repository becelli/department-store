import sqlite3 as sql
from datetime import datetime, timedelta
from model.classes import (
    user as u,
    product as p,
    sale as s,
    payment as pm,
    provider as pr,
)
import random as random


class Database(object):
    """
    Database class.
    """

    def __init__(self, db_name):
        """
        Initialize the database.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connect to the database.
        """
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close(self):
        """
        Close the connection to the database.
        """
        self.connection.close()

    def execute(self, query, params=None):
        """
        Execute a query.
        """
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetch(self):
        """
        Fetch the results of a query.
        """
        return self.cursor.fetchall()

    def fetch_one(self):
        """
        Fetch one result of a query.
        """
        return self.cursor.fetchone()

    def commit(self):
        """
        Commit the changes to the database.
        """
        self.connection.commit()

    # CREATE TABLES
    def create_product_tables(self):
        self.connect()
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type = 'food' OR type = 'electronic' OR type = 'clothing' OR type = 'homeappliance'),
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                fabrication_date TEXT NOT NULL,
                price REAL NOT NULL,
                provider_id INTEGER NOT NULL,
                is_available INTEGER NOT NULL,
                FOREIGN KEY(provider_id) REFERENCES provider(id)
            )
            """
        )
        self.commit()

        # Fashion
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS fashion (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(id) REFERENCES product(id)
            )"""
        )
        self.commit()

        # Electronics
        self.execute(
            """CREATE TABLE IF NOT EXISTS electronic (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(id) REFERENCES product(id)
            )"""
        )
        self.commit()

        # Food
        self.execute(
            """CREATE TABLE IF NOT EXISTS food (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(id) REFERENCES product(id)
            )"""
        )
        self.commit()

        # Home Appliances
        self.execute(
            """CREATE TABLE IF NOT EXISTS home_appliance (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(id) REFERENCES product(id)
            )"""
        )
        self.commit()

        self.close()

    def create_user_tables(self):
        self.connect()
        self.execute(
            """CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type = 'customer' OR type = 'provider'),
                name TEXT NOT NULL,
                cpf TEXT NOT NULL,
                rg TEXT NOT NULL,
                birth_date DATE NOT NULL,
                address TEXT NOT NULL,
                zipcode TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS seller (
                id INTEGER PRIMARY KEY,
                salary REAL NOT NULL,
                pis TEXT NOT NULL,
                admission_date TEXT NOT NULL,
                FOREIGN KEY(id) REFERENCES user(id)
            )
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS customer (
                id INTEGER PRIMARY KEY,
                is_golden_customer INTEGER NOT NULL,
                FOREIGN KEY(id) REFERENCES user(id)
            )
            """
        )
        self.commit()

        self.close()

    def create_provider_tables(self):
        self.connect()
        self.execute(
            """ 
            CREATE TABLE IF NOT EXISTS provider (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
            """
        )
        self.commit()
        self.close()

    def create_sale_tables(self):
        self.connect()
        self.execute(
            """CREATE TABLE IF NOT EXISTS sale (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                seller_id INTEGER NOT NULL,
                sell_date TEXT NOT NULL,
                payment_method_id INTEGER NOT NULL,
                FOREIGN KEY(seller_id) REFERENCES seller(id)
                FOREIGN KEY(payment_method_id) REFERENCES payment_method(id)
            )"""
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS sold_product (
                sale_id PRIMARY KEY,
                id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES sale(id) ON DELETE CASCADE,
                FOREIGN KEY(id) REFERENCES product(id)
            )"""
        )
        self.commit()

        self.close()

    def create_payment_method_tables(self):
        self.connect()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS payment_method(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )"""
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS credit_card (
                id INTEGER PRIMARY KEY,
                flag TEXT NOT NULL,
                number TEXT NOT NULL CHECK(LENGTH(number) = 16),
                FOREIGN KEY(id) REFERENCES payment_method(id)
            )
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS cash (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(id) REFERENCES payment_method(id)
            )"""
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS pix (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL,
                FOREIGN KEY(id) REFERENCES payment_method(id)
            )
            """
        )
        self.commit()

        self.close()

    # SELECT DATA
    def _select_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM product WHERE id = ?", (id,))
        product = self.fetch_one()
        self.close()
        return product

    def _select_user_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM user WHERE id = ?", (id,))
        user = self.fetch_one()
        self.close()
        return user

    def _select_provider_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM provider WHERE id = ?", (id,))
        provider = self.fetch_one()
        self.close()
        return provider

    def _select_seller_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM seller WHERE id = ?", (id,))
        seller = self.fetch_one()
        self.close()
        return seller

    def _select_customer_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM customer WHERE id = ?", (id,))
        customer = self.fetch_one()
        self.close()
        return customer

    # TODO IT RIGHT?
    def _select_payment_method_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM payment_method WHERE id = ?", (id,))
        payment_method = self.fetch_one()
        self.close()
        return payment_method

    # SINGLE RESULT
    def select_by_id(self, id: int) -> p.Product:
        self.connect()
        self.execute("SELECT id, type FROM product WHERE id = ?", (id,))
        product = self.fetch_one()
        self.close()

        if product is None:
            return None
        if product["type"] == "food":
            return self.select_food_by_id(product["id"])
        elif product["type"] == "electronic":
            return self.select_electronic_by_id(product["id"])
        elif product["type"] == "home_appliance":
            return self.select_home_appliance_by_id(product["id"])
        elif product["type"] == "clothing":
            return self.select_clothing_by_id(product["id"])
        return None

    def select_food_by_id(self, id: int) -> p.Food:
        self.connect()
        self.execute("SELECT * FROM food WHERE id = ?", (id,))
        food = self.fetch_one()
        product = self._select_data_by_id(food["id"])
        self.close()
        if food is None:
            return None

        provider = self._select_provider_data_by_id(food["provider_id"])
        return p.Food(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            provider=provider,
            is_available=food["is_available"],
            id=food["id"],
        )

    def select_electronic_by_id(self, id: int) -> p.Electronic:
        self.connect()
        self.execute("SELECT * FROM electronic WHERE id = ?", (id,))
        electronic = self.fetch_one()
        product = self._select_data_by_id(electronic["id"])
        self.close()

        if electronic is None:
            return None

        provider = self._select_provider_data_by_id(product["provider_id"])
        return p.Electronic(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            provider=provider,
            is_available=electronic["is_available"],
            id=electronic["id"],
        )

    def select_home_appliance_by_id(self, id: int) -> p.HomeAppliance:
        self.connect()
        self.execute("SELECT * FROM home_appliance WHERE id = ?", (id,))
        home_appliance = self.fetch_one()
        product = self._select_data_by_id(home_appliance["id"])
        self.close()

        if home_appliance is None:
            return None

        provider = self._select_provider_data_by_id(product["provider_id"])
        return p.HomeAppliance(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            provider=provider,
            is_available=home_appliance["is_available"],
            id=home_appliance["id"],
        )

    def select_clothing_by_id(self, id: int) -> p.Clothing:
        self.connect()
        self.execute("SELECT * FROM clothing WHERE id = ?", (id,))
        cloth = self.fetch_one()
        product = self._select_data_by_id(cloth["id"])
        self.close()

        if cloth is None:
            return None

        provider = self._select_provider_data_by_id(product["provider_id"])
        return p.Clothing(
            name=product["name"],
            description=product["description"],
            fabrication=product["fabrication"],
            price=product["price"],
            provider=provider,
            is_available=cloth["is_available"],
            id=cloth["id"],
        )

    def select_customer_by_id(self, id: int) -> u.Customer:
        self.connect()
        self.execute("SELECT * FROM customer WHERE id = ?", (id,))
        customer = self.fetch_one()
        self.close()
        if customer is None:
            return None
        user = self._select_user_data_by_id(customer["user_id"])
        return u.Customer(
            id=user["id"],
            name=user["name"],
            cpf=user["cpf"],
            rg=user["rg"],
            birth_date=user["birth_date"],
            address=user["address"],
            zipcode=user["zipcode"],
            email=user["email"],
            is_golden_customer=customer["is_golden_customer"],
        )

    def select_seller_by_id(self, id: int) -> u.Seller:
        self.connect()
        self.execute("SELECT * FROM seller WHERE id = ?", (id,))
        seller = self.fetch_one()
        self.close()
        if seller is None:
            return None
        user = self._select_user_data_by_id(seller["user_id"])
        return u.Seller(
            name=user["name"],
            cpf=user["cpf"],
            rg=user["rg"],
            birth_date=user["birth_date"],
            address=user["address"],
            zipcode=user["zipcode"],
            email=user["email"],
            salary=seller["salary"],
            pis=seller["pis"],
            admission_date=seller["admission_date"],
            id=user["id"],
        )

    def select_provider_by_id(self, id: int) -> p.Provider:
        self.connect()
        self.execute("SELECT * FROM provider WHERE id = ?", (id,))
        provider = self.fetch_one()
        self.close()
        if provider is None:
            return None
        return p.Provider(
            cnpj=provider["cnpj"],
            name=provider["name"],
            description=provider["description"],
            address=provider["address"],
            zipcode=provider["zipcode"],
            email=provider["email"],
            id=provider["id"],
        )

    def select_sale_item_by_id(self, id: int) -> s.SaleItem:
        self.connect()
        self.execute("SELECT * FROM sale_item WHERE id = ?", (id,))
        sale_item = self.fetch_one()
        self.close()
        if sale_item is None:
            return None
        return s.SaleItem(
            self.select_by_id(sale_item["id"]),
            sale_item["quantity"],
            sale_item["id"],
        )

    def select_sale_by_id(self, id: int) -> s.Sale:
        self.connect()
        self.execute("SELECT * FROM sale WHERE id = ?", (id,))
        sale = self.fetch_one()
        self.close()
        if sale is None:
            return None

        return s.Sale(
            customer=self.select_customer_by_id(sale["customer_id"]),
            seller=self.select_seller_by_id(sale["seller_id"]),
            sell_date=sale["date"],
            itens=self._iterator_append(sale["items"], self.select_sale_item_by_id),
            payment_mathod=None,  # TODO
            id=sale["id"],
        )

    def select_payment_method_by_id(self, id: int) -> pm.Payment:
        self.connect()
        self.execute("SELECT * FROM payment_method WHERE id = ?", (id,))
        payment_method = self.fetch_one()
        self.close()
        if payment_method is None:
            return None

    # MULTIPLE
    def select_all_products(self) -> list[p.Product]:
        self.connect()
        self.execute("SELECT id FROM product")
        products = self.fetch_all()
        self.close()
        return self._iterator_append(products, self._select_by_id)

    def select_all_foods(self) -> list[p.Food]:
        self.connect()
        self.execute("SELECT id FROM food")
        foods = self.fetch_all()
        self.close()
        return self._iterator_append(foods, self._select_food_by_id)

    def select_all_electronics(self) -> list[p.Electronic]:
        self.connect()
        self.execute("SELECT id FROM electronic")
        electronics = self.fetch_all()
        self.close()
        return [
            self._select_electronic_by_id(electronic["id"])
            for electronic in electronics
        ]

    def select_all_home_appliances(self) -> list[p.HomeAppliance]:
        self.connect()
        self.execute("SELECT id FROM home_appliance")
        home_appliances = self.fetch_all()
        self.close()
        return [
            self._select_home_appliance_by_id(home_appliance["id"])
            for home_appliance in home_appliances
        ]

    def select_all_clothes(self) -> list[p.Clothing]:
        self.connect()
        self.execute("SELECT id FROM clothing")
        clothes = self.fetch_all()
        self.close()
        return self._iterator_append(clothes, self.select_clothing_by_id)

    def select_all_customers(self) -> list[u.Customer]:
        self.connect()
        self.execute("SELECT id FROM customer")
        customers = self.fetch_all()
        self.close()
        return self._iterator_append(customers, self.select_customer_by_id)

    def select_all_sellers(self) -> list[u.Seller]:
        self.connect()
        self.execute("SELECT id FROM seller")
        sellers = self.fetch_all()
        self.close()
        sellers = []
        return self._iterator_append(sellers, self.select_seller_by_id)

    def select_all_providers(self) -> list[p.Provider]:
        self.connect()
        self.execute("SELECT id FROM provider")
        providers = self.fetch_all()
        self.close()
        return self._iterator_append(providers, self.select_provider_by_id)

    def select_all_golden_customers(self) -> list[u.Customer]:
        self.connect()
        self.execute("SELECT id FROM customers WHERE is_golden_customer = 1")
        customers = self.fetch_all()
        self.close()
        return self._iterator_append(customers, self.select_customer_by_id)

    def _iterator_append(self, data, function):
        data_list = []
        iterator = iter(data)
        while True:
            try:
                it = next(iterator)
                data_list.append(function(it))
            except StopIteration:
                break
        return data_list

    # RANDOM
    def select_random_customer(self) -> u.Customer:
        self.connect()
        self.execute("SELECT id FROM customer")
        customers = self.fetch_all()
        self.close()
        c = self._select_customer_data_by_id(random.choice(customers))
        return u.Customer(
            name=c["name"],
            cpf=c["cpf"],
            rg=c["rg"],
            birthdate=c["birth_date"],
            address=c["address"],
            zipcode=c["zipcode"],
            email=c["email"],
            is_golden=c["is_golden_customer"],
            id=c["id"],
        )

    def select_random_seller(self) -> u.Seller:
        self.connect()
        self.execute("SELECT id FROM seller")
        seller = self.fetch_all()
        self.close()
        s = self._select_customer_data_by_id(random.choice(seller))
        return u.Seller(
            name=s["name"],
            cpf=s["cpf"],
            rg=s["rg"],
            birthdate=s["birth_date"],
            address=s["address"],
            zipcode=s["zipcode"],
            email=s["email"],
            id=s["id"],
        )

    def select_random_products(self):
        products = self.select_all_products()
        shuffled = random.shuffle(products)
        quantity = random.randint(1, len(products))
        return shuffled[:quantity]

    # SPECIAL LISTS
    def select_customer_history_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM sale WHERE customer_id = ?", (id,))
        sales = self.fetch_all()
        self.close()
        return self._iterator_append(sales, self._select_sale_by_id)

    def select_best_seller_of_the_month(self, month: int, year: int):
        # Select the seller with the most sales
        self.connect()
        self.execute(
            f"SELECT seller_id FROM sale WHERE date LIKE '{year}-{month}%' GROUP BY seller_id ORDER BY COUNT(*) DESC LIMIT 1"
        )
        seller_id = self.fetch_one()["seller_id"]
        self.close()
        return self.select_seller_by_id(seller_id)

    def select_all_sales(self):
        self.connect()
        self.execute("SELECT id FROM sale")
        sales = self.fetch_all()
        self.close()
        return self._iterator_append(sales, self.select_sale_by_id)

    def select_all_sales_in_month(self, month: int, year: int):
        self.connect()
        self.execute(f"SELECT id FROM sale WHERE date LIKE '{year}-{month}%'")
        sales_ids = self.fetch_all()
        self.close()
        sales = self._iterator_append(sales_ids, self.select_sale_by_id)

        iterator = iter(sales)
        sum = 0
        while True:
            try:
                obj: s.Sale = next(iterator)
                sum += obj.calculate_total_value()
            except StopIteration:
                break
        return sum

    def _select_all_sales_paid_with(self, table: str) -> list[s.Sale]:
        self.connect()
        self.execute(f"SELECT id FROM {table}")
        cash_ids = self.fetch_all()["id"]
        ids = ",".join(cash_ids)[1:-1]

        print(ids)  # TODO remove it
        self.execute(f"SELECT id FROM sale WHERE 0id IN ({ids})")
        sales = self.fetch_all()["id"]
        self.close()
        return self._iterator_append(sales, self.select_sale_by_id)

    def select_all_sales_paid_via_cash(self) -> list[s.Sale]:
        return self._select_all_sales_paid_with("cash")

    def select_all_sales_paid_via_card(self) -> list[s.Sale]:
        return self._select_all_sales_paid_with("credit_card")

    def select_all_sales_paid_via_pix(self) -> list[s.Sale]:
        return self._select_all_sales_paid_with("pix")

    # select most sold products
    def select_most_sold_products(self, n: int = 10) -> list[p.Product]:
        self.connect()
        self.execute(
            f"SELECT id, COUNT(*) AS total FROM sale GROUP BY id ORDER BY total DESC LIMIT {n}"
        )
        products = self.fetch_all()
        self.close()
        return self._iterator_append(products, self.select_by_id)

    def insert_product(self, product: p.Product):
        type: str = product.__class__.__name__.lower()

        self.connect()
        self.execute(
            "INSERT INTO product (type, name, description, fabrication_date, price, provider_id, is_available) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                type,
                product.get_name(),
                product.get_description(),
                product.get_fabrication_date(),
                product.get_price(),
                product.get_provider_id(),
                product.get_is_available(),
            ),
        )
        self.commit()

        row = self.lastrowid
        self.execute(
            f"INSERT INTO {type} (id) VALUES (?)",
            (row,),
        )
        self.commit()
        self.close()

    def insert_provider(self, provider: p.Provider):
        self.connect()
        self.execute(
            "INSERT INTO provider (cnpj, name, description, email, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
            (
                provider.get_cnpj(),
                provider.get_name(),
                provider.get_description(),
                provider.get_email(),
                provider.get_phone(),
                provider.get_address(),
            ),
        )
        self.commit()
        self.close()

    def insert_user(self, user: u.User) -> int:
        type = user.__class__.__name__.lower()
        self.connect()
        self.execute(
            "INSERT INTO user (type, name, cpf, rg, birth_date, address, zipcode, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                type,
                user.get_name(),
                user.get_cpf(),
                user.get_rg(),
                user.get_birthdate(),
                user.get_address(),
                user.get_zipcode(),
                user.get_email(),
            ),
        )
        self.commit()

        row = self.lastrowid
        if type == "customer":
            self.execute(
                f"INSERT INTO customer (id, is_golden_customer) VALUES (?)",
                (row, user.is_golden_customer()),
            )
        elif type == "seller":
            self.execute(
                f"INSERT INTO seller (id, salary, pis, admission_date) VALUES (?, ?, ?, ?)",
                (row, user.get_salary(), user.get_pis(), user.get_admission_date()),
            )

        self.commit()
        self.close()

    def insert_sale_item(self, sale_item: s.SaleItem) -> int:
        self.connect()
        self.execute(
            "INSERT INTO sale_item (sale_id, id, quantity, price) VALUES (?, ?, ?, ?)",
            (
                sale_item.get_sale_id(),
                sale_item.get_id().get_id(),
                sale_item.get_quantity(),
                sale_item.get_price(),
            ),
        )
        self.commit()
        self.close()

    def insert_sale(self, sale: s.Sale) -> int:
        self.connect()
        self.execute(
            "INSERT INTO sale (customer_id, seller_id, 0id, date) VALUES (?, ?, ?, ?)",
            (
                sale.get_customer().get_id(),
                sale.get_seller().get_id(),
                sale.get_payment_method().get_id(),
                sale.get_date(),
            ),
        )
        row = self.lastrowid
        self.commit()
        self.close()
        return row

    def select_all_payment_methods(self) -> list[pm.Payment]:
        self.connect()
        self.execute("SELECT id FROM payment_method")
        payment_methods = self.fetch_all()["id"]
        self.close()
        return self._iterator_append(payment_methods, self.select_payment_method_by_id)

    def insert_payment_method(self, payment_method: pm.Payment):
        type = payment_method.__class__.__name__.lower()
        self.connect()
        self.execute(
            "INSERT INTO payment_method (name) VALUES (?)",
            (payment_method.get_name(),),
        )
        self.commit()
        self.close()
        # TODO INSERT cash, pix and card

    def populate_database(self, n: int = 10):
        import extra.random as rand

        r = rand.RandomObject()

        i = 0
        while i < n:  # Insert random users (customers, sellers)
            c = r.Customer()
            s = r.Seller()
            self.insert_user(c)
            self.insert_user(s)
            i += 1

        i = 0
        while i < n:  # Insert providers
            p = r.Provider()
            self.insert_provider(p)
            i += 1

        i = 0
        while i < n:  # Insert random products (food, electronics, clothes, etc)
            p = r.Product()
            self.insert_product(p)
            i += 1

        i = 0
        # while i < n:  # Insert random sales
        #     pass
        # si = r.Sale_item()

        # Insert random sales (by consequence, payments)
