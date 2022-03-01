from datetime import date
from model.classes.user import Customer, Seller
from model.classes.payment import Payment
from model.classes.product import Product


class SaleItem:
    def __init__(
        self,
        product: Product,
        quantity: int,
        # price: float, #TODO WONT BE IMPLEMENTED
        id: int = None,
    ):
        self._product = product
        self._quantity = quantity
        self._id = id

    def __str__(self):
        return (
            f"Item: {self._get_id()}"
            f"\n Produto: {self._get_product_id()}"
            f"\n Quantidade: {self._get_quantity()}"
            f"\n Preço: {self._get_price()}"
        )

    def get_id(self):
        return self._id

    def get_product_id(self):
        return self._product_id

    def get_quantity(self):
        return self._quantity

    def _set_id(self, id):
        self._id = id

    def set_product_id(self, product: Product):
        self._product = product

    def set_quantity(self, quantity):
        self._quantity = quantity

    def calculate_total_value(self):
        return self._quantity * self.product.calculate_value()


class Sale:
    def __init__(
        self,
        customer: Customer,
        seller: Seller,
        sell_date: date,
        payment_mathod: Payment,
        id: int = None,
    ):
        self._customer = customer
        self._seller = seller
        self._sell_date = sell_date
        self._payment_mathod = payment_mathod
        self._id = id

    def __str__(self):
        return (
            f"Venda: {self._get()}: {self._get_sell_date()}"
            f"\n Customere: {self._get_customer()}"
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

    def set_payment_mathod(self, payment_mathod):
        self._payment_mathod = payment_mathod

    def add_item(self, item):
        self._itens.append(item)

    def get_total_value(self):
        total = 0
        iterator = iter(self._itens)
        while True:
            try:
                item = next(iterator)
                total += item.get_value()
            except StopIteration:
                break
        return total

    def get_discount(self):
        value = self.get_total_value()
        return value * 0.02 if self.customer.get_is_golden() else 0.0

    def calculate_total_value(self):
        return self.get_total_value() - self.get_discount()
