"""A module representing the stack-based calculator.

Written by Aaron Barge
Copyright 2022
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Any

import calculator.operators as ops
from calculator.error import CalculatorError, OperatorError


@dataclass
class Calculator:
    stack: list[Any] = field(default_factory=list)

    def __repr__(self) -> str:
        result = "Calculator(["
        for index, elem in enumerate(self.stack):
            if index != 0:
                result += ", "
            if callable(elem):
                result += elem.__qualname__
            else:
                result += str(elem)
        result += "])"
        return result

    def append(self, value: Any) -> None:
        self.stack.append(value)

    def pop(self) -> None:
        self.stack.pop()

    def validate(self) -> int:
        result = 0
        for curr in self.stack:

            if callable(curr) or type(curr) in [int, float]:
                result += 1
            elif isinstance(curr, ops.Operator):
                result -= curr.args - 1
            else:
                raise CalculatorError(f"Invalid symbol found in stack: {curr}, type={type(curr)}")

            if result < 1:
                raise CalculatorError(f"Stack could not properly calculate result")

        return result

    def calculate(self, *args, **kwargs) -> float:
        num_stack = deque()
        for index, curr in enumerate(self.stack):
            if callable(curr):
                num_stack.append(curr(*args, **kwargs))
            elif type(curr) in [int, float]:
                num_stack.append(curr)
            elif isinstance(curr, ops.Operator):
                vals = []
                for _ in range(curr.args):
                    vals.append(num_stack.pop())
                try:
                    val = curr.apply(*vals)
                except Exception as e:
                    op_error = OperatorError()
                    op_error.failed_index = index
                    raise op_error
                num_stack.append(val)
            else:
                raise CalculatorError(f"Invalid symbol found in stack: {curr}")
        if len(num_stack) != 1:
            raise CalculatorError(f"Stack could not properly calculate result")
        return num_stack[0]

    def optimize(self) -> None:
        """Some day...
        while True:
            match self.stack:
                case [*head, a, b, ops.Operator(repr=_, args=2, func=func), *tail] if type(a) in [int, float] and a != math.pi and type(b) in [int, float] and b != math.pi:
                    self.stack = head + [func(b, a)] + tail
                case [*head, a, ops.Operator(repr=_, args=1, func=func), *tail] if type(a) in [int, float] and a != math.pi:
                    self.stack = head + [func(a)] + tail
                case _:
                    return
        """

    def clear(self) -> None:
        self.stack = []

    def to_latex(self) -> str:
        stack = deque()
        for curr in self.stack:
            if callable(curr):
                stack.append(curr.__name__)
            elif type(curr) in [int, float]:
                if curr == math.pi:
                    stack.append("\\pi")
                else:
                    stack.append(str(curr))
            elif isinstance(curr, ops.Operator):
                vals = []
                for _ in range(curr.args):
                    vals.append(stack.pop())
                val = curr.latex(*vals)
                stack.append(val)
            else:
                raise CalculatorError(f"Invalid symbol found in stack: {curr}")
        return stack[0]
