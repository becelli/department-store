class Payment:
    def __init__(self, payment_type: str, id: int = None):

        self._payment_type = payment_type
        self._id = id

    def __str__(self):
        f"Tipo de pagamento: {self.get_payment_type}"

    def get_payment_type(self):
        return self._payment_type

    def set_payment_type(self, type: str):
        self._payment_type = type

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id


class Cash(Payment):
    def __init__(self, payment_type: str, id: int = None):
        super().__init__(payment_type, id)
        self._payment_type = payment_type
        self._id = id


class CreditCard(Payment):
    def __init__(self, payment_type: str, name, flag, number: int, id: int = None):
        super().__init__(payment_type, id)
        self._payment_type = payment_type
        self._id = id
        self._name = name
        self._flag = flag
        self._number = number

    def get_name(self):
        return self._name

    def get_flag(self):
        return self._flag

    def get_number(self):
        return self._number

    def set_name(self, name: str):
        self._name = name

    def set_flag(self, flag: str):
        self._flag = flag

    def set_number(self, number: int):
        self.set_number = number

    def __str__(self):
        super().__str__()
        +f"Nome do cartão: {self.get_name}"
        +f"Numero do cartão: {self.get_number}"
        +f"Bandeira do cartão: {self.get_flag}"


class Pix(Payment):
    def __init__(self, payment_type: str, code: str, id: int = None):
        super().__init__(payment_type, id)
        self._payment_type = payment_type
        self._id = id
        self._code = code

    def get_code(self):
        return self._code

    def set_code(self, code: str):
        self._code = code

    def __str__(self):
        super().__str__()
        +f"\nCódigo PIX: {self._code}"
