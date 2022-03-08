import model.classes.database as database
from model.classes.user import Customer, Seller


class UserController:
    def __init__(self, db: str = "app.db"):
        self.db = database.Database(db)

    def add_user(self, user) -> int:
        return self.db.insert_user(user)

    def get_all_customers(self) -> list[Customer]:
        return self.db.select_all_customers()

    def get_random_customer(self) -> Customer:
        return self.db.select_random_customer()

    def get_customer_by_id(self, id: int) -> Customer:
        return self.db.select_customer_by_id(id)

    def get_all_golden_customers(self) -> list[Customer]:
        return self.db.select_all_golden_customers()

    def get_customer_history_by_id(self, id: int):
        return self.db.select_customer_history_by_id(id)

    def get_seller_by_id(self, id: int) -> Seller:
        return self.db.select_seller_by_id(id)

    def get_best_seller_of_the_month(self, month: str, year: str) -> list[Seller, int]:
        return self.db.select_best_seller_of_the_month(month, year)

    def get_all_sellers(self) -> list[Seller]:
        return self.db.select_all_sellers()

    def get_random_seller(self) -> Seller:
        return self.db.select_random_seller()
