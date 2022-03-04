from abc import ABC, abstractmethod
from datetime import date
from model.classes.provider import Provider


class Product(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication_date: date,
        price: float,
        provider: Provider,
        is_available: bool = True,
        id: int = None,
    ):
        self._name = name
        self._description = description
        self._fabrication_date = fabrication_date
        self._price = price
        self._provider = provider
        self._is_available = is_available
        self._id = id

    def __str__(self):
        return (
            f"Produto {self._id}: {self._name}"
            f"\nDescrição: {self._description}"
            f"\nFabricação: {self._fabrication_date}"
            f"\nPreço: {round(self._price, 2)}"
            # f"\nFornecedor: {self._provider.get_name()}"
            f"\nDisponível: {'Sim' if self._is_available else 'Não'}\n"
        )

    @abstractmethod
    def calculate_value():
        pass

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_fabrication_date(self):
        return self._fabrication_date

    def get_price(self):
        return self._price

    def get_provider(self) -> Provider:
        return self._provider

    def get_is_available(self):
        return self._is_available

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_description(self, description):
        self._description = description

    def set_fabrication_date(self, fabrication_date):
        self._fabrication_date = fabrication_date

    def set_price(self, price):
        self._price = price

    def set_provider(self, provider):
        self._provider = provider

    def set_is_available(self, available):
        self._is_available = available


class Food(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication_date: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication_date, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.005


class Home_Appliance(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication_date: str,
        price: float,
        provider: Provider,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication_date, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.02


class Electronic(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication_date: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication_date, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.045


class Clothing(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication_date: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication_date, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.0125
