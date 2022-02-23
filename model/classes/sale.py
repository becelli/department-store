from datetime import date
import controller.user as uc
from model.classes.user import Client, Seller
from model.classes.payment import Payment


class Sale:
    def __init__(
        self,
        customer: Client,
        seller: Seller,
        sell_date: date,
        itens: list,  # SaleItem
        total_value: float,
        discount: float,
        payment_mathod: Payment,
        id: int = None,
    ):
        self._customer = customer
        self._seller = seller
        self._sell_date = sell_date
        self._itens = itens
        self._total_value = total_value
        self._discount = discount
        self._payment_mathod = payment_mathod
        self. = id

    def __str__(self):
        return (
            f"Venda: {self._get()}: {self._get_sell_date()}"
            f"\n Cliente: {self._get_customer()}"
            f"\n Vendedor: {self._get_seller()}"
            f"\n Valor Total: {self._get_total_value()}"
            f"\n Desconto: {self._get_discount()}"
            f"\n Forma de Pagamento: {self._get_payment_mathod()}"
        )

    def get_id(self):
        return self._id

    def get_customer(self):
        return self._customer

    def get_seller(self):
        return self._seller

    def get_sell_date(self):
        return self._sell_date

    def get_itens(self):
        return self._itens

    def get_total_value(self):
        return self._total_value

    def get_discount(self):
        return self._discount

    def get_payment_mathod(self):
        return self._payment_mathod

    def set_id(self, id):
        self.id = id

    def set_customer(self, customer):
        self._customer = customer

    def set_seller(self, seller):
        self._seller = seller

    def set_sell_date(self, sell_date):
        self._sell_date = sell_date

    def set_itens(self, itens):
        self._itens = itens

    def set_total_value(self, total_value):
        self._total_value = total_value

    def set_discount(self, discount):
        self._discount = discount

    def set_payment_mathod(self, payment_mathod):
        self._payment_mathod = payment_mathod

    def add_item(self, item):
        self._itens.append(item)

    def total_value(self):
        total = 0
        iterator = iter(self._itens)
        while True:
            try:
                item = next(iterator)
                total += item.get_value()
            except StopIteration:
                break
        # 2% of discount for golden customer
        return total * 0.98 if self.customer.get_is_golden() else total
