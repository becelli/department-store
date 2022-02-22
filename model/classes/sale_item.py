class SaleItem:
    def __init__(
        self,
        product_id: int,
        quantity: int,
        price: float,
        id: int = None,
    ):
        self._product_id = product_id
        self._quantity = quantity
        self._price = price
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

    def get_price(self):
        return self._price

    def set_id(self, id):
        self._id = id

    def set_product_id(self, product_id):
        self._product_id = product_id

    def set_quantity(self, quantity):
        self._quantity = quantity

    def set_price(self, price):
        self._price = price

    def calculate_total_value(self):
        return self._quantity * self._price
