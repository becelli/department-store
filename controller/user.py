import model.classes.user as user
import model.classes.database as database


class UserController:
    def __init__(self, db: str = "app.db"):
        self.db = database.Database(db)

    def insert_user(self, user) -> int:
        return self.db.insert_user(user)

    def _select_user_data_by_id(self):
        return self.db._select_user_data_by_id()

    def select_all_customer(self):
        return self.db.select_all_customers()

    def select_random_customer(self):
        return self.db.select_random_customer()

    def select_customer_data_by_id(self, id: int):
        return self.db._select_customer_data_by_id(id)

    def select_customer_by_id(self, id: int):
        return self.db.select_customer_by_id(id)

    def select_all_golden_customers(self):
        return self.db.select_all_golden_customers()

    def select_customer_history_by_id(self, id: int):
        return self.db.select_customer_history_by_id(id)

    def select_seller_by_id(self, id: int):
        return self.db.select_seller_by_id(id)

    def _select_seller_data_by_id(self, id: int):
        return self.db._select_seller_data_by_id(self, id)

    def select_best_seller_of_the_month(self, month: int, year: int):
        return self.db.select_best_seller_of_the_month(month, year)

    def select_all_sellers(self):
        return self.db.select_all_sellers()

    def select_random_seller(self):
        return self.db.select_random_seller()
