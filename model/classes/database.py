from re import S
import sqlite3
from datetime import datetime, timedelta


class Database(object):
    """
    Database class.
    """

    def __init__(self, db_name):
        """
        Initialize the database.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the database.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Close the connection to the database.
        """
        self.conn.close()

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
        self.conn.commit()

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
                address TEXT NOT NULL,
            )
            """
        )
        self.commit()
        self.close()

    def create_sale_tables(self):
        self.connect()
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS sales(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               customer_id INTEGER NOT NULL,
               seller_id INTEGER NOT NULL,
               sell_date TEXT NOT NULL,
               total_value REAL NOT NULL,
               discount REAL NOT NULL,
               FOREIGN KEY(seller_id) REFERENCES sellers(id),
               FOREGIN KEY(payment_mathod_id) REFERENCES payment_methods(id)
               
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS products_sold (
                sale_id PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )"""
        )
        self.commit()

        self.close()

    def create_product_tables(self):
        self.connect()
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                fabrication_date TEXT NOT NULL,
                price REAL NOT NULL,
                provider_id INTEGER NOT NULL,
                is_available INTEGER NOT NULL,
                FOREIGN KEY(provider_id) REFERENCES providers(id)
            )
            """
        )
        self.commit()

        # Fashion
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS fashion (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(product_id) REFERENCES products(id)
            """
        )
        self.commit()

        # Electronics
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS electronic (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(product_id) REFERENCES products(id)
            """
        )
        self.commit()

        # Food
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS food (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(product_id) REFERENCES products(id)
            """
        )
        self.commit()

        # Home Appliances
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS home_appliances (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(product_id) REFERENCES products(id)
            """
        )
        self.commit()

        self.close()

    def create_user_tables(self):
        self.connect()
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cpf TEXT NOT NULL,
                rg TEXT NOT NULL,
                birth_date DATE NOT NULL,
                address TEXT NOT NULL,
                zipcode TEXT NOT NULL,
                email TEXT NOT NULL,
        """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS sellers (
                id INTEGER PRIMARY KEY,
                salary REAL NOT NULL,
                pis TEXT NOT NULL,
                admission_date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                is_golden_customer INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            """
        )
        self.commit()

        self.close()

    def create_payment_method_tables(self):
        self.connect()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS payment_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS credit_card (
                id INTEGER PRIMARY KEY,
                flag TEXT NOT NULL,
                number TEXT NOT NULL CHECK(LENGTH(number) = 16),
                FORIGN KEY(payment_method_id) REFERENCES payment_methods(id),
            )
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS cash (
                id INTEGER PRIMARY KEY,
                FOREIGN KEY(payment_method_id) REFERENCES payment_methods(id)
            """
        )
        self.commit()

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS pix (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL,
                FOREIGN KEY(payment_method_id) REFERENCES payment_methods(id)
            )
            """
        )
        self.commit()

        self.close()

    def select_user_data_by_id(self, id):
        self.connect()
        self.execute("SELECT * FROM users WHERE id = ?", (id,))
        user = self.fetch_one()
        self.close()
        return user

    def select_product_data_by_id(self, id):
        self.connect()
        self.execute("SELECT * FROM products WHERE id = ?", (id,))
        product = self.fetch_one()
        self.close()
        return product
