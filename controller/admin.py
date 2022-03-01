import model.classes.database as db


class DatabaseController:
    def __init__(self, db_name):
        self.db = db.Database(db_name)

    def create_provider_tables(self):
        return self.db.create_provider_tables()

    def create_product_tables(self):
        return self.db.create_product_tables()

    def create_user_tables(self):
        return self.db.create_user_tables()

    def create_sale_tables(self):
        return self.db.create_sale_tables()

    def create_payment_method_tables(self):
        return self.db.create_payment_method_tables()
