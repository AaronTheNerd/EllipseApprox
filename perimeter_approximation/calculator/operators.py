"""A module for containing the operators for the calculator.

Written by Aaron Barge
Copyright 2022
"""


import math
from typing import Callable


class Operator:
    def __init__(
        self,
        repr: str,
        args: int,
        func: Callable[..., float],
        constrain: Callable[..., bool],
        latex: Callable[..., str],
    ):
        self.repr = repr
        self.args = args
        self.func = func
        self.constrain = constrain
        self.latex = latex

    def __repr__(self) -> str:
        return self.repr

    def apply(self, *args) -> float:
        return self.func(*args)

    def constrain(self, a, b) -> bool:
        return self.constrain(a, b)

    def to_latex(self, *args) -> str:
        return self.latex(*args)


ADD_OP = Operator(
    "ops.ADD_OP", 2, lambda a, b: a + b, lambda a, b: b == 0, lambda a, b: f"({a}+{b})"
)
SUB_OP = Operator(
    "ops.SUB_OP", 2, lambda a, b: a - b, lambda a, b: False, lambda a, b: f"({a}-{b})"
)
MUL_OP = Operator(
    "ops.MUL_OP", 2, lambda a, b: a * b, lambda a, b: b == 1, lambda a, b: f"({a}\\times{b})"
)
DIV_OP = Operator(
    "ops.DIV_OP",
    2,
    lambda a, b: a / b,
    lambda a, b: a == 0 or (a == 1 and b == 1),
    lambda a, b: f"\\frac{{{a}}}{{{b}}}",
)
EXP_OP = Operator("ops.EXP_OP", 2, math.pow, lambda a, b: False, lambda a, b: f"({{{a}}}^{{{b}}})")
NEG_OP = Operator("ops.NEG_OP", 1, lambda a: -a, lambda a, b: b == 0, lambda a: f"(-{a})")
SQRT_OP = Operator(
    "ops.SQRT_OP",
    1,
    math.sqrt,
    lambda a, b: b in [0, 1]
    or (type(a) in [int, float] and a > 0 and b == NEG_OP)
    or (type(b) in [int, float] and b < 0),
    lambda a: f"\\sqrt{{{a}}}",
)
INV_OP = Operator(
    "ops.INV_OP",
    1,
    lambda a: 1 / a,
    lambda a, b: b == 0 or b == 1,
    lambda a: f"\\frac{{{1}}}{{{a}}}",
)
