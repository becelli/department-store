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
