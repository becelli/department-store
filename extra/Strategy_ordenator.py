from abc import ABC, abstractmethod
from model.classes import product as p


class StrategySort:
    def __init__(self, method: str) -> None:
        self.method = method

    def sort(self, array: list[p.Product]) -> list:
        if self.method == "bubble":
            return self.bubble_sort(array)
        elif self.method == "insertion":
            return self.insertion_sort(array)
        raise ValueError("Método de ordenação inválido")

    def _bubble_sort(self, array: list[p.Product]) -> list:
        for i in range(len(array)):
            for j in range(len(array) - 1):
                if array[j].calculate_value() > array[j + 1].calculate_value():
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def _insertion_sort(self, array: list[p.Product]) -> list:
        for i in range(len(array)):
            j = i
            while j > 0 and array[j].calculate_value() < array[j - 1].calculate_value():
                array[j], array[j - 1] = array[j - 1], array[j]
                j -= 1
        return array
