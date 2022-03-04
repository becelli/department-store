import model.classes.database as database
import model.classes.sale as sale


class SaleController:
    def __init__(self, db: str = "app.db"):
        self.db = database.Database(db)

    def select_sale_item_by_id(self):
        return self.db.select_sale_item_by_id()

    def select_sale_by_id(self):
        return self.db.select_sale_by_id()

    def select_all_sales(self):
        return self.db.select_all_sales()

    def select_all_sales_in_month(self, month: int, year: int):
        return self.db.select_all_sales_in_month(month, year)

    def select_all_sales_paid_via_cash(self):
        return self.db.select_all_sales_paid_via_cash()

    def select_all_sales_paid_via_card(self):
        return self.db.select_all_sales_paid_via_card()

    def select_all_sales_paid_via_pix(self):
        return self.db.select_all_sales_paid_via_pix()
