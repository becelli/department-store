from datetime import date


class Sale:
    def __init__(
        self,
        customer_id: int,
        seller_id: int,
        sell_date: date,
        itens: list,  # SaleItem
        total_value: float,
        discount: float,
        payment_mathod_id: int,
        id: int = None,
    ):
        self._customer_id = customer_id
        self._seller_id = seller_id
        self._sell_date = sell_date
        self._itens = itens
        self._total_value = total_value
        self._discount = discount
        self._payment_mathod_id = payment_mathod_id
        self._id = id

    def __str__(self):
        return (
            f"Venda: {self._get_id()}: {self._get_sell_date()}"
            f"\n Cliente: {self._get_customer_id()}"
            f"\n Vendedor: {self._get_seller_id()}"
            f"\n Valor Total: {self._get_total_value()}"
            f"\n Desconto: {self._get_discount()}"
            f"\n Forma de Pagamento: {self._get_payment_mathod_id()}"
        )

    def get_id(self):
        return self._id

    def get_customer_id(self):
        return self._customer_id

    def get_seller_id(self):
        return self._seller_id

    def get_sell_date(self):
        return self._sell_date

    def get_itens(self):
        return self._itens

    def get_total_value(self):
        return self._total_value

    def get_discount(self):
        return self._discount

    def get_payment_mathod_id(self):
        return self._payment_mathod_id

    def set_id(self, id):
        self._id = id

    def set_customer_id(self, customer_id):
        self._customer_id = customer_id

    def set_seller_id(self, seller_id):
        self._seller_id = seller_id

    def set_sell_date(self, sell_date):
        self._sell_date = sell_date

    def set_itens(self, itens):
        self._itens = itens

    def set_total_value(self, total_value):
        self._total_value = total_value

    def set_discount(self, discount):
        self._discount = discount

    def set_payment_mathod_id(self, payment_mathod_id):
        self._payment_mathod_id = payment_mathod_id

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
        return total
