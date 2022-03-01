from abc import ABC, abstractmethod
from datetime import date


class User(ABC):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birthdate: date,
        address: str,
        zipcode: str,
        email: str,
        id: int = None,
    ):

        self._name = name
        self._cpf = cpf
        self._rg = rg
        self._birthdate = birthdate
        self._address = address
        self._zipcode = zipcode
        self._email = email
        self._id = id

    @abstractmethod
    def __str__(self):
        return (
            f"Usuario: {self._get_id()}: {self._get_name()}"
            f"\n RG: {self._get_rg()}"
            f"\n CPF: {self._get_cpf()}"
            f"\n Email: {self._get_email()}"
            f"\n CEP: {self._get_zipcode()}"
            f"\n Endereço: {self._get_address()}"
            f"\n Nascimento: {self._get_birthdate()}"
        )

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_cpf(self):
        return self._cpf

    def get_rg(self):
        return self._rg

    def get_birthdate(self):
        return self._birthdate

    def get_zipcode(self):
        return self._zipcode

    def get_email(self):
        return self._email

    def get_address(self):
        return self._address

    def set_name(self, name: str):
        self._name = name

    def set_id(self, id: str):
        self._id = id

    def set_cpf(self, cpf: str):
        self._cpf = cpf

    def set_rg(self, rg: str):
        self._rg = rg

    def set_birthdate(self, birthdate: date):
        self._birthdate = birthdate

    def set_zipcode(self, zipcode: str):
        self._zipcode = zipcode

    def set_email(self, email: str):
        self._email = email

    def set_address(self, address: str):
        self._address = address


class Seller(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birthdate: date,
        address: str,
        zipcode: str,
        email: str,
        salary: float,
        pis: str,
        admission_date: date,
        id: int = None,
    ):
        super().__init__(name, cpf, rg, birthdate, address, zipcode, email, id)
        self._salary = salary
        self._pis = pis
        self._admission_date = admission_date

    def __str__(self):
        return (
            super().__str__()
            + f"\n Salário: {self._get_salary()}"
            + f"\n PIS: {self._get_pis()}"
            + f"\n Data de Admissão: {self._get_admission_date()}"
        )

    def get_salary(self):
        return self._salary

    def get_pis(self):
        return self._pis

    def get_admission_date(self):
        return self._admission_date

    def set_salary(self, salary: float):
        self._salary = salary

    def set_pis(self, pis: str):
        self._pis = pis

    def set_admission_date(self, admission_date: date):
        self._admission_date = admission_date


class Customer(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birthdate: date,
        address: str,
        zipcode: str,
        email: str,
        is_golden: bool,
        id: int = None,
    ):
        super().__init__(name, cpf, rg, birthdate, address, zipcode, email, id)
        self._is_golden = is_golden

    def __str__(self):
        return (
            super().__str__()
            + f"\n Cliente Ouro: {'Sim' if self._get_is_golden() else 'Não'}"
        )

    def get_is_golden(self):
        return self._is_golden

    def set_is_golden(self, is_golden: bool):
        self._is_golden = is_golden
