# Written by Aaron Barge
# Copyright 2022

import math

from utils import double_factorial


class EllipseProperties:
    def __init__(self, a: float = 1, b: float = 1) -> None:
        self._a = a
        self._b = b

    def a(self) -> float:
        return self._a

    def b(self) -> float:
        return self._b

    def h(self) -> float:
        return ((self.a() - self.b()) / (self.a() + self.b())) ** 2

    def e(self) -> float:
        return math.sqrt(self.a() ** 2 - self.b() ** 2) / self.a()

    def c(self) -> float:
        return self.e() * self.a()

    def circumference(self, precision: int = 5) -> float:
        result = 1
        for n in range(1, precision + 1):
            result += (
                (double_factorial(2 * n - 1) / (2**n * math.factorial(n))) ** 2
                * self.h() ** n
                / (2 * n - 1) ** 2
            )
        return result * math.pi * (self.a() + self.b())
