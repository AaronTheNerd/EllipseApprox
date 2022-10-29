import os
from functools import reduce
from itertools import cycle
from typing import Any, Callable


def double_factorial(x: int) -> int:
    result = 1
    for i in range(1, x + 1):
        if i % 2 == x % 2:
            result *= i
    return result


def percent_error(expected: float, calculated: float) -> float:
    return abs((calculated - expected) / expected) * 100


def seed_factory() -> int:
    return int.from_bytes(os.urandom(8), byteorder="big")


def divide_list(items: list[Any], amount: int) -> list[list[Any]]:
    baskets = [[] for _ in range(min(amount, len(items)))]
    for item, basket in zip(items, cycle(baskets)):
        basket.append(item)
    return baskets

def all(funcs: list[Callable[[Any], bool]]) -> Callable[[Any], bool]:
    return lambda x: reduce(lambda a, b: a and b, [func(x) for func in funcs])
