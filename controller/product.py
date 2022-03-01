from model.classes import product
from model.classes.database import Database
from model.classes import (
    product as p,
)


class ProductController:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def select_all_products(self) -> list[product.Product]:
        return self.db.select_all_products()

    def select_product_data_by_id(self, id):
        return self.db._select_product_data_by_id(id)

    def select_product_by_id(self, id):
        return self.db.select_product_by_id(id)

    def select_random_product(self):
        return self.db.select_random_products()

    def select_most_sold_products(self):
        return self.db.select_most_sold_products()

    def insert_product(self, product: p.Product):
        return self.db.insert_product(p.Product)
