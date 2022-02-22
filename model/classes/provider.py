class Provider:  # Fornecedor
    def __init__(
        self,
        cnpj: str,
        name: str,
        description: str,
        email: str,
        phone: str,
        address: str,
        id: int = None,
    ):

        self._cnpj = cnpj
        self._name = name
        self._description = description
        self._email = email
        self._phone = phone
        self._address = address
        self._id = id

    def __str__(self):
        return (
            f"Fornecedor {self._id}: {self._name}"
            f"\n CNPJ: {self._cnpj}"
            f"\n Email: {self._email}"
            f"\n Telefone: {self._phone}"
            f"\n Endereço: {self._address}"
            f"\n Descrição: {self._description}"
        )

    def get_id(self):
        return self._id

    def get_cnpj(self):
        return self._cnpj

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_email(self):
        return self._email

    def get_phone(self):
        return self._phone

    def get_address(self):
        return self._address

    def set_id(self, id):
        self._id = id

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj

    def set_name(self, name):
        self._name = name

    def set_description(self, description):
        self._description = description

    def set_email(self, email):
        self._email = email

    def set_phone(self, phone):
        self._phone = phone

    def set_address(self, address):
        self._address = address
