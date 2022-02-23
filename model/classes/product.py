from abc import ABC, abstractmethod
from model.classes.provider import Provider


class Product(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication: str,
        price: float,
        provider: Provider,
        available: bool = True,
        id: int = None,
    ):
        self._name = name
        self._description = description
        self._fabrication = fabrication
        self._price = price
        self._provider = provider
        self._available = available
        self._id = id

    def __str__(self):
        return (
            f"Produto {self._id}: {self._name}"
            f"\nDescrição: {self._description}"
            f"\nFabricação: {self._fabrication}"
            f"\nPreço: {self._price}"
            f"\nFornecedor: {self._provider.get_name()}"
            f"\nDisponível: {'Sim' if self._available else 'Não'}"
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

    def get_fabrication(self):
        return self._fabrication

    def get_price(self):
        return self._price

    def get_provider(self):
        return self._provider

    def get_available(self):
        return self._available

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_description(self, description):
        self._description = description

    def set_fabrication(self, fabrication):
        self._fabrication = fabrication

    def set_price(self, price):
        self._price = price

    def set_provider(self, provider):
        self._provider = provider

    def set_available(self, available):
        self._available = available


class Food(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.005


class HomeAppliances(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.02


class Electronics(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.045


class Clothes(Product):
    def __init__(
        self,
        name: str,
        description: str,
        fabrication: str,
        price: float,
        provider: str,
        is_available: bool = True,
        id: int = None,
    ):
        super().__init__(
            name, description, fabrication, price, provider, is_available, id
        )

    def calculate_value(self):
        return self._price * 1.0125
