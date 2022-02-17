class Product:
    def __init__(
        self, id, name, description, fabrication, price, provider, is_available
    ):
        self.id = id
        self.name = name
        self.description = description
        self.fabrication = fabrication
        self.price = price
        self.provider = provider
        self.is_available = is_available

    def __str__(self):
        return (
            f"Produto {self.id}: {self.name}"
            f"\nDescrição: {self.description}"
            f"\nFabricação: {self.fabrication}"
            f"\nPreço: {self.price}"
            f"\nFornecedor: {self.provider}"
            f"\nDisponível: {self.is_available}"
        )
