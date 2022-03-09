from datetime import date
from model.classes.user import Customer, Seller
from model.classes.payment import Payment
from model.classes.product import Product


class SaleItem:
    def __init__(
        self,
        product: Product,
        quantity: int,
        id: int = None,
    ):
        self._product: Product = product
        self._quantity: float = quantity
        self._id = id

    def __str__(self):
        return (
            f"Item: {self.get_id()}"
            f"\nProduto: {self.get_product().get_name()}"
            f"\nQuantidade: {self.get_quantity()}"
            f"\nPreço: {round(self.calculate_total_value(), 2)}"
        )

    def get_id(self):
        return self._id

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def _set_id(self, id):
        self._id = id

    def set_product(self, product: Product):
        self._product = product

    def set_quantity(self, quantity):
        self._quantity = quantity

    def calculate_total_value(self):
        return self.get_quantity() * self.get_product().calculate_value()


class Sale:
    def __init__(
        self,
        customer: Customer,
        seller: Seller,
        date: date,
        itens: list[SaleItem],
        payment_method: Payment,
        id: int = None,
    ):
        self._customer = customer
        self._seller = seller
        self._date = date
        self._itens = itens
        self._payment_method = payment_method
        self._id = id

    def __str__(self):
        return (
            f"Venda: {self.get()}: {self.get_date()}"
            f"\nClente: {self.get_customer()}"
            f"\nVendedor: {self.get_seller()}"
            f"\nValor Total: {self.get_total_value()}"
            f"\nDesconto: {self.get_discount()}"
            f"\nForma de Pagamento: {self.get_payment_method()}"
        )

    def get_id(self):
        return self._id

    def get_customer(self):
        return self._customer

    def get_seller(self):
        return self._seller

    def get_date(self):
        return self._date

    def get_itens(self):
        return self._itens

    def get_discount(self):
        return self._discount

    def get_payment_method(self):
        return self._payment_method

    def set_id(self, id):
        self.id = id

    def set_customer(self, customer):
        self._customer = customer

    def set_seller(self, seller):
        self._seller = seller

    def set_date(self, date):
        self._date = date

    def set_itens(self, itens):
        self._itens = itens

    def set_payment_method(self, payment_method):
        self._payment_method = payment_method

    def add_item(self, item):
        self._itens.append(item)

    def get_total_value(self):
        total = 0
        iterator = iter(self.get_itens())
        while True:
            try:
                item: SaleItem = next(iterator)
                total += item.calculate_total_value()
            except StopIteration:
                break
        return total

    def get_discount(self):
        value = self.get_total_value()
        return value * (0.02 if self._customer.get_is_golden() else 0.0)

    def calculate_total_value(self):
        return self.get_total_value() - self.get_discount()
