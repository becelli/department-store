from model.classes.database import Database
from model.classes.sale import Sale


class SaleController:
    def __init__(self, db: str = "app.db"):
        self.db = Database(db)

    def get_sale_by_id(self, id):
        return self.db.select_sale_by_id(id)

    def get_all_sales(self) -> list[Sale]:
        return self.db.select_all_sales()

    def get_all_sales_in_month(self, month: int, year: int):
        return self.db.select_all_sales_in_month(month, year)

    def get_all_sales_paid_via_cash(self):
        return self.db.select_all_sales_paid_via_cash()

    def get_all_sales_paid_via_card(self):
        return self.db.select_all_sales_paid_via_card()

    def get_all_sales_paid_via_pix(self):
        return self.db.select_all_sales_paid_via_pix()

    def insert_payment(self, payment: Sale) -> int:
        return self.db.insert_payment_method(payment)

    def insert_sale(self, sale: Sale):
        return self.db.insert_sale(sale)

    def get_customer_history(self, id: int):
        return self.db.select_customer_history_by_id(id)
