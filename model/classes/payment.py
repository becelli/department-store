class payment:
    def __init__(self, payment_type: str, id):

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
