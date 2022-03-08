from model.classes.database import Database
from model.classes.product import Clothing, Electronic, Food, Home_Appliance, Product


class ProductController:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def get_all_products(self) -> list[Product]:
        return self.db.select_all_products()

    def get_all_foods(self) -> list[Food]:
        return self.db.select_all_foods()

    def get_all_clothes(self) -> list[Clothing]:
        return self.db.select_all_clothes()

    def get_all_electronics(self) -> list[Electronic]:
        return self.db.select_all_electronics()

    def get_all_home_appliances(self) -> list[Home_Appliance]:
        return self.db.select_all_home_appliances()

    def get_product_data_by_id(self, id):
        return self.db._select_product_data_by_id(id)

    def get_product_by_id(self, id):
        return self.db.select_product_by_id(id)

    def get_random_product(self):
        return self.db.select_random_products()

    def get_most_sold_products(self):
        return self.db.select_most_sold_products()

    def add_product(self, product: Product):
        return self.db.insert_product(product)
