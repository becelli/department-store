import sqlite3 as sql
import random as random
from model.classes.payment import Payment
from model.classes.product import Clothing, Electronic, Food, Home_Appliance, Product
from model.classes.provider import Provider
from model.classes.sale import Sale, SaleItem
from model.classes.user import Customer, Seller, User


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

    def fetch_all(self):
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

    def lastrowid(self):
        try:
            return self.cursor.lastrowid
        except:
            self.connect()
            self.execute("SELECT last_insert_rowid()")
            id = self.fetch_one()[0]
            self.close()
            return id

    # CREATE TABLES
    def create_product_tables(self):
        self.connect()
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type = 'food' OR type = 'electronic' OR type = 'clothing' OR type = 'home_appliance'),
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
            CREATE TABLE IF NOT EXISTS clothing (
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
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                cpf TEXT NOT NULL,
                rg TEXT NOT NULL,
                birthdate DATE NOT NULL,
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
                is_golden BOOLEAN NOT NULL,
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
                date TEXT NOT NULL,
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
    def _select_product_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM product WHERE id = ?", (id,))
        product = self.fetch_one()
        self.close()
        # create a dict with the product data
        return {
            "id": product[0],
            "type": product[1],
            "name": product[2],
            "description": product[3],
            "fabrication_date": product[4],
            "price": product[5],
            "provider_id": product[6],
            "is_available": product[7],
        }

    def _select_user_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM user WHERE id = ?", (id,))
        user = self.fetch_one()
        self.close()
        return {
            "id": user[0],
            "type": user[1],
            "name": user[2],
            "cpf": user[3],
            "rg": user[4],
            "birthdate": user[5],
            "address": user[6],
            "zipcode": user[7],
            "email": user[8],
        }

    def _select_provider_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM provider WHERE id = ?", (id,))
        provider = self.fetch_one()
        self.close()
        return {
            "id": provider[0],
            "cnpj": provider[1],
            "name": provider[2],
            "description": provider[3],
            "email": provider[4],
            "phone": provider[5],
            "address": provider[6],
        }

    def _select_seller_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM seller WHERE id = ?", (id,))
        seller = self.fetch_one()
        self.close()
        return {
            "id": seller[0],
            "salary": seller[1],
            "pis": seller[2],
        }

    def _select_customer_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM customer WHERE id = ?", (id,))
        customer = self.fetch_one()
        self.close()
        return {
            "id": customer[0],
            "is_golden": customer[1],
        }

    # TODO IT RIGHT?
    def _select_payment_method_data_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM payment_method WHERE id = ?", (id,))
        payment_method = self.fetch_one()
        self.close()
        return {
            "id": payment_method[0],
            "name": payment_method[1],
        }

    # SINGLE RESULT
    def select_product_by_id(self, id: int) -> Product:
        self.connect()
        self.execute("SELECT id, type FROM product WHERE id = ?", (id,))
        product = self.fetch_one()
        self.close()

        if product is None:
            return None
        if product[1] == "food":
            return self.select_food_by_id(product[0])
        elif product[1] == "electronic":
            return self.select_electronic_by_id(product[0])
        elif product[1] == "home_appliance":
            return self.select_home_appliance_by_id(product[0])
        elif product[1] == "clothing":
            return self.select_clothing_by_id(product[0])
        return None

    def select_food_by_id(self, id: int) -> Food:
        self.connect()
        self.execute("SELECT * FROM food WHERE id = ?", (id,))
        p = self.fetch_one()
        if p is None:
            return None

        product = self._select_product_data_by_id(id)
        provider = self.select_provider_by_id(product["provider_id"])

        return Food(
            name=product["name"],
            description=product["description"],
            fabrication_date=product["fabrication_date"],
            price=product["price"],
            provider=provider,
            is_available=product["is_available"],
            id=product["id"],
        )

    def select_electronic_by_id(self, id: int) -> Electronic:
        self.connect()
        self.execute("SELECT * FROM electronic WHERE id = ?", (id,))
        p = self.fetch_one()
        if p is None:
            return None

        product = self._select_product_data_by_id(id)
        provider = self._select_provider_data_by_id(product["provider_id"])
        return Electronic(
            name=product["name"],
            description=product["description"],
            fabrication_date=product["fabrication_date"],
            price=product["price"],
            provider=provider,
            is_available=product["is_available"],
            id=product["id"],
        )

    def select_home_appliance_by_id(self, id: int) -> Home_Appliance:
        self.connect()
        self.execute("SELECT * FROM home_appliance WHERE id = ?", (id,))
        p = self.fetch_one()
        if p is None:
            return None

        product = self._select_product_data_by_id(id)
        provider = self._select_provider_data_by_id(product["provider_id"])
        return Home_Appliance(
            name=product["name"],
            description=product["description"],
            fabrication_date=product["fabrication_date"],
            price=product["price"],
            provider=provider,
            is_available=product["is_available"],
            id=product["id"],
        )

    def select_clothing_by_id(self, id: int) -> Clothing:
        self.connect()
        self.execute("SELECT * FROM clothing WHERE id = ?", (id,))
        p = self.fetch_one()
        if p is None:
            return None

        product = self._select_product_data_by_id(id)
        provider = self._select_provider_data_by_id(product["provider_id"])
        return Clothing(
            name=product["name"],
            description=product["description"],
            fabrication_date=product["fabrication_date"],
            price=product["price"],
            provider=provider,
            is_available=product["is_available"],
            id=product["id"],
        )

    def select_customer_by_id(self, id: int) -> Customer:
        self.connect()
        self.execute("SELECT * FROM customer WHERE id = ?", (id,))
        query = self.fetch_one()
        self.close()
        if query is None:
            return None
        [id, is_golden] = query
        user = self._select_user_data_by_id(id)
        return Customer(
            id=user["id"],
            name=user["name"],
            cpf=user["cpf"],
            rg=user["rg"],
            birthdate=user["birthdate"],
            address=user["address"],
            zipcode=user["zipcode"],
            email=user["email"],
            is_golden=is_golden,
        )

    def select_seller_by_id(self, id: int) -> Seller:
        self.connect()
        self.execute("SELECT * FROM seller WHERE id = ?", (id,))
        query = self.fetch_one()
        self.close()
        if query is None:
            return None
        [id, salary, pis, admission_date] = query
        user = self._select_user_data_by_id(id)
        return Seller(
            name=user["name"],
            cpf=user["cpf"],
            rg=user["rg"],
            birthdate=user["birthdate"],
            address=user["address"],
            zipcode=user["zipcode"],
            email=user["email"],
            salary=salary,
            pis=pis,
            admission_date=admission_date,
            id=user["id"],
        )

    def select_provider_by_id(self, id: int) -> Provider:
        self.connect()
        self.execute("SELECT * FROM provider WHERE id = ?", (id,))
        query = self.fetch_one()
        self.close()
        if query is None:
            return None
        [id, cnpj, name, description, email, phone, address] = query
        return Provider(
            cnpj=cnpj,
            name=name,
            description=description,
            email=email,
            phone=phone,
            address=address,
            id=id,
        )

    def select_sale_item_by_id(self, id: int) -> SaleItem:
        self.connect()
        self.execute("SELECT * FROM sale_item WHERE id = ?", (id,))
        sale_item = self.fetch_one()
        self.close()
        if sale_item is None:
            return None
        return SaleItem(
            self.select_by_id(sale_item["id"]),
            sale_item["quantity"],
            sale_item["id"],
        )

    def select_sale_by_id(self, id: int) -> Sale:
        self.connect()
        self.execute("SELECT * FROM sale WHERE id = ?", (id,))
        sale = self.fetch_one()
        self.close()
        if sale is None:
            return None

        return Sale(
            customer=self.select_customer_by_id(sale["customer_id"]),
            seller=self.select_seller_by_id(sale["seller_id"]),
            sell_date=sale["date"],
            itens=self._iterator_append(sale["items"], self.select_sale_item_by_id),
            payment_mathod=None,  # TODO
            id=sale["id"],
        )

    def select_payment_method_by_id(self, id: int) -> Payment:
        self.connect()
        self.execute("SELECT * FROM payment_method WHERE id = ?", (id,))
        payment_method = self.fetch_one()
        self.close()
        if payment_method is None:
            return None

    # MULTIPLE
    def select_all_products(self) -> list[Product]:
        self.connect()
        self.execute("SELECT id FROM product")
        products = [x[0] for x in self.fetch_all()]
        self.close()

        return self._iterator_append(products, self.select_product_by_id)

    def select_all_foods(self) -> list[Food]:
        self.connect()
        self.execute("SELECT id FROM food")
        foods = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(foods, self.select_food_by_id)

    def select_all_electronics(self) -> list[Electronic]:
        self.connect()
        self.execute("SELECT id FROM electronic")
        electronics = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(electronics, self.select_electronic_by_id)

    def select_all_home_appliances(self) -> list[Home_Appliance]:
        self.connect()
        self.execute("SELECT id FROM home_appliance")
        home_appliances = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(home_appliances, self.select_home_appliance_by_id)

    def select_all_clothes(self) -> list[Clothing]:
        self.connect()
        self.execute("SELECT id FROM clothing")
        clothes = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(clothes, self.select_clothing_by_id)

    def select_all_customers(self) -> list[Customer]:
        self.connect()
        self.execute("SELECT id FROM customer")
        customers = [x[0] for x in self.fetch_all()]
        self.close()

        return self._iterator_append(customers, self.select_customer_by_id)

    def select_all_sellers(self) -> list[Seller]:
        self.connect()
        self.execute("SELECT id FROM seller")
        sellers = [x[0] for x in self.fetch_all()]
        self.close()

        return self._iterator_append(sellers, self.select_seller_by_id)

    def select_all_providers(self) -> list[Provider]:
        self.connect()
        self.execute("SELECT id FROM provider")
        providers = [x[0] for x in self.fetch_all()]  # iterator
        self.close()
        return self._iterator_append(providers, self.select_provider_by_id)

    def select_all_golden_customers(self) -> list[Customer]:

        self.connect()
        self.execute("SELECT id FROM customer WHERE is_golden = 1")
        customers = [x[0] for x in self.fetch_all()]
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
    def select_random_customer(self) -> Customer:
        self.connect()
        self.execute("SELECT id FROM customer")
        customers = [x[0] for x in self.fetch_all()]
        self.close()
        c = self._select_customer_data_by_id(random.choice(customers))
        return Customer(
            name=c["name"],
            cpf=c["cpf"],
            rg=c["rg"],
            birthdate=c["birthdate"],
            address=c["address"],
            zipcode=c["zipcode"],
            email=c["email"],
            is_golden=c["is_golden"],
            id=c["id"],
        )

    def select_random_seller(self) -> Seller:
        self.connect()
        self.execute("SELECT id FROM seller")
        seller = [x[0] for x in self.fetch_all()]
        self.close()
        s = self._select_customer_data_by_id(random.choice(seller))
        return Seller(
            name=s["name"],
            cpf=s["cpf"],
            rg=s["rg"],
            birthdate=s["birthdate"],
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

    def select_random_provider(self):
        self.connect()
        self.execute("SELECT id FROM provider")
        provider = [x[0] for x in self.fetch_all()]
        self.close()
        s = self._select_provider_data_by_id(random.choice(provider))

        return Provider(
            cnpj=s["cnpj"],
            name=s["name"],
            description=s["description"],
            email=s["email"],
            phone=s["phone"],
            address=s["address"],
            id=s["id"],
        )

    # SPECIAL LISTS
    def select_customer_history_by_id(self, id: int):
        self.connect()
        self.execute("SELECT * FROM sale WHERE customer_id = ?", (id,))
        sales = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(sales, self._select_sale_by_id)

    def select_best_seller_of_the_month(self, month: int, year: int) -> Seller:
        # Select the seller with the most sales
        self.connect()
        self.execute(
            f"SELECT seller_id, COUNT(*) as total FROM sale WHERE date LIKE '{year}-{month}%' GROUP BY seller_id ORDER BY total DESC LIMIT 1"
        )
        query = self.fetch_one()
        self.close()
        if query is None:
            return None
        [seller_id, quantity] = query
        return [self.select_seller_by_id(seller_id), quantity]

    def select_all_sales(self):
        self.connect()
        self.execute("SELECT id FROM sale")
        sales = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(sales, self.select_sale_by_id)

    def select_all_sales_in_month(self, month: int, year: int):
        self.connect()
        self.execute(f"SELECT id FROM sale WHERE date LIKE '{year}-{month}%'")
        sales_ids = [x[0] for x in self.fetch_all()]
        self.close()
        sales = self._iterator_append(sales_ids, self.select_sale_by_id)

        iterator = iter(sales)
        sum = 0
        while True:
            try:
                obj: Sale = next(iterator)
                sum += obj.calculate_total_value()
            except StopIteration:
                break
        return sum

    def _select_all_sales_paid_with(self, table: str) -> list[Sale]:
        self.connect()
        self.execute(f"SELECT id FROM {table}")
        cash_ids = [x[0] for x in self.fetch_all()]
        ids = ",".join(cash_ids)[1:-1]

        print(ids)  # TODO remove it
        self.execute(f"SELECT id FROM sale WHERE id IN ({ids})")
        sales = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(sales, self.select_sale_by_id)

    def select_all_sales_paid_via_cash(self) -> list[Sale]:
        return self._select_all_sales_paid_with("cash")

    def select_all_sales_paid_via_card(self) -> list[Sale]:
        return self._select_all_sales_paid_with("credit_card")

    def select_all_sales_paid_via_pix(self) -> list[Sale]:
        return self._select_all_sales_paid_with("pix")

    # select most sold products
    def select_most_sold_products(self, n: int = 10) -> list[Product]:
        self.connect()
        self.execute(
            f"SELECT id, COUNT(*) AS total FROM sale GROUP BY id ORDER BY total DESC LIMIT {n}"
        )
        products = [x[0] for x in self.fetch_all()]
        print(products)  # TODO remove it. Just checking if it returns only one value.
        self.close()
        return self._iterator_append(products, self.select_product_by_id)

    def insert_product(self, product: Product):
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
                product.get_provider().get_id(),
                product.get_is_available(),
            ),
        )
        self.commit()

        row = self.lastrowid()
        self.execute(
            f"INSERT INTO {type} (id) VALUES (?)",
            (row,),
        )
        self.commit()
        self.close()

    def insert_provider(self, provider: Provider):
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

    def insert_user(self, user: User) -> int:
        type = user.__class__.__name__.lower()

        self.connect()
        self.execute(
            "INSERT INTO user (type, name, cpf, rg, birthdate, address, zipcode, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                type,
                user.get_name(),
                user.get_cpf(),
                user.get_rg(),
                str(user.get_birthdate())[:10],
                user.get_address(),
                user.get_zipcode(),
                user.get_email(),
            ),
        )

        row = self.lastrowid()
        if type == "customer":
            self.execute(
                f"INSERT INTO customer (id, is_golden) VALUES (?, ?)",
                (row, user.get_is_golden()),
            )
        elif type == "seller":
            self.execute(
                f"INSERT INTO seller (id, salary, pis, admission_date) VALUES (?, ?, ?, ?)",
                (row, user.get_salary(), user.get_pis(), user.get_admission_date()),
            )

        self.commit()
        self.close()

    def insert_sale_item(self, sale_item: SaleItem) -> int:
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

    def insert_sale(self, sale: Sale) -> int:
        self.connect()
        self.execute(
            "INSERT INTO sale (customer_id, seller_id, id, date) VALUES (?, ?, ?, ?)",
            (
                sale.get_customer().get_id(),
                sale.get_seller().get_id(),
                sale.get_payment_method().get_id(),
                sale.get_date(),
            ),
        )
        row = self.lastrowid()
        self.commit()
        self.close()
        return row

    def select_all_payment_methods(self) -> list[Payment]:
        self.connect()
        self.execute("SELECT id FROM payment_method")
        payment_methods = [x[0] for x in self.fetch_all()]
        self.close()
        return self._iterator_append(payment_methods, self.select_payment_method_by_id)

    def insert_payment_method(self, payment_method: Payment):
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

        r = rand.RandomObject(
            product_db=self.db_name, user_db=self.db_name, provider_db=self.db_name
        )

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

            a = 0
            self.insert_product(p)
            i += 1

        i = 0
        # while i < n:  # Insert random sales
        #     pass
        # si = r.Sale_item()

        # Insert random sales (by consequence, payments)
