import math
from dataclasses import dataclass, field
from typing import Any, Optional

import calculator.operators as ops
from calculator.calculator import Calculator
from ellipse import EllipseProperties


@dataclass
class Approximates:
    _approxes: dict[str, Calculator] = field(default_factory=dict)

    def register(self, name: str, approx: Calculator) -> tuple[bool, str, Calculator]:
        result = False
        if name not in self._approxes.keys():
            result = True
            self._approxes[name] = approx
        return (result, name, self._approxes[name])

    def getAll(self):
        return self._approxes

    def __getitem__(self, name: str) -> Optional[Calculator]:
        if name in self._approxes:
            return self._approxes[name]
        return None


APPROXIMATES = Approximates()


APPROXIMATES.register(
    "Average",
    Calculator(
        [
            EllipseProperties.a,  # [a]
            EllipseProperties.b,  # [a, b]
            ops.ADD_OP,  # [a + b]
            math.pi,  # [a + b, pi]
            ops.MUL_OP,  # [(a + b)pi]
        ]
    ),
)  # 2 * pi * (a + b) / 2


APPROXIMATES.register(
    "GeometricMean",
    Calculator(
        [
            EllipseProperties.a,  # [a]
            EllipseProperties.b,  # [a, b]
            ops.MUL_OP,  # [ab]
            ops.SQRT_OP,  # [sqrt(ab)]
            2,  # [sqrt(ab), 2]
            math.pi,  # [sqrt(ab), 2, pi]
            ops.MUL_OP,  # [sqrt(ab), 2pi]
            ops.MUL_OP,  # [sqrt(ab)2pi]
        ]
    ),
)  # 2 * pi * sqrt(ab)


APPROXIMATES.register(
    "Simple",
    Calculator(
        [
            2,  # [2]
            2,  # [2, 2]
            EllipseProperties.a,  # [2, 2, a]
            ops.EXP_OP,  # [2, a^2]
            2,  # [2, a^2, 2]
            EllipseProperties.b,  # [2, a^2, 2, b]
            ops.EXP_OP,  # [2, a^2, b^2]
            ops.ADD_OP,  # [2, a^2 + b^2]
            ops.DIV_OP,  # [(a^2 + b^2) / 2]
            ops.SQRT_OP,  # [sqrt((a^2 + b^2) / 2)]
            2,  # [sqrt((a^2 + b^2) / 2), 2]
            math.pi,  # [sqrt((a^2 + b^2) / 2), 2, pi]
            ops.MUL_OP,  # # [sqrt((a^2 + b^2) / 2), 2pi]
            ops.MUL_OP,  # [sqrt((a^2 + b^2) / 2)2pi]
        ]
    ),
)  # 2 * pi * sqrt((a^2 + b^2) / 2)


APPROXIMATES.register(
    "Ramanujan1",
    Calculator(
        [
            3,
            EllipseProperties.a,
            ops.MUL_OP,  # 3a
            EllipseProperties.b,
            ops.ADD_OP,  # 3a + b
            3,
            EllipseProperties.b,
            ops.MUL_OP,  # 3b
            EllipseProperties.a,
            ops.ADD_OP,  # 3b + a
            ops.MUL_OP,  # (3a + b)(3b + a)
            ops.SQRT_OP,  # sqrt((3a + b)(3b + a))
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,  # a + b
            3,
            ops.MUL_OP,  # 3(a + b)
            ops.SUB_OP,  # 3(a + b) - sqrt((3a + b)(3b + a))
            math.pi,
            ops.MUL_OP,  # pi(3(a + b) - sqrt((3a + b)(3b + a)))
        ]
    ),
)  # pi * [3(a + b) - sqrt((3a + b)(a + 3b))]


APPROXIMATES.register(
    "MattParker1",
    Calculator(
        [
            2,
            EllipseProperties.a,
            ops.EXP_OP,  # a^2
            269,
            ops.MUL_OP,  # 269a^2
            667,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.MUL_OP,  # ab
            ops.MUL_OP,  # 667ab
            ops.ADD_OP,  # 269a^2 + 667ab
            2,
            EllipseProperties.b,
            ops.EXP_OP,  # b^2
            371,
            ops.MUL_OP,  # 371b^2
            ops.ADD_OP,  # 269a^2 + 667ab + 371b^2
            ops.SQRT_OP,  # sqrt(269a^2 + 667ab + 371b^2)
            3,
            53,
            EllipseProperties.a,
            ops.MUL_OP,  # 53a
            ops.DIV_OP,  # 53a/3
            35,
            717,
            EllipseProperties.b,
            ops.MUL_OP,  # 717b
            ops.DIV_OP,  # 717b/35
            ops.ADD_OP,  # 717b/35 + 53a/3
            ops.SUB_OP,  # 717b/35 + 53a/3 - sqrt(269a^2 + 667ab + 371b^2)
            math.pi,
            ops.MUL_OP,  # pi(717b/35 + 53a/3 - sqrt(269a^2 + 667ab + 371b^2))
        ]
    ),
)  # pi * [53a / 3 + 717b / 35 - sqrt(269a^2 + 667ab + 371b^2)]


APPROXIMATES.register(
    "Ramanujan2",
    Calculator(
        [
            3,
            EllipseProperties.h,
            ops.MUL_OP,  # 3h
            4,
            ops.SUB_OP,  # 4 - 3h
            ops.SQRT_OP,  # sqrt(4 - 3h)
            10,
            ops.ADD_OP,  # 10 + sqrt(4 - 3h)
            3,
            EllipseProperties.h,
            ops.MUL_OP,  # 3h
            ops.DIV_OP,  # 3h / (10 + sqrt(4 - 3h))
            1,
            ops.ADD_OP,  # 1 + 3h / (10 + sqrt(4 - 3h))
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,  # a + b,
            ops.MUL_OP,  # (a + b)(1 + 3h / (10 + sqrt(4 - 3h)))
            math.pi,
            ops.MUL_OP,  # pi(a + b)(1 + 3h / (10 + sqrt(4 - 3h)))
        ]
    ),
)  # pi(a + b)(1 + 3h / (10 + sqrt(4 - 3h)))


APPROXIMATES.register(
    "MattParkerLazy",
    Calculator(
        [
            5,
            6,
            EllipseProperties.a,
            ops.MUL_OP,  # 6a
            ops.DIV_OP,  # 6a / 5
            4,
            3,
            EllipseProperties.b,
            ops.MUL_OP,  # 3b
            ops.DIV_OP,  # 3b / 4
            ops.ADD_OP,  # 3b / 4 + 6a / 5
            math.pi,
            ops.MUL_OP,  # pi(3b / 4 + 6a / 5)
        ]
    ),
)  # pi * (6a / 5 + 3b / 4)


APPROXIMATES.register(
    "Sixth",
    Calculator(
        [
            3.141592653589793,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,  # [pi(a + b)]
            ops.INV_OP,  # [1/(pi(a + b))]
            6,
            EllipseProperties.h,  # [1/(pi(a + b)), 6, h]
            ops.ADD_OP,  # [1/(pi(a + b)), h + 6,]
            10,  # [1/(pi(a + b)), h + 6, 10]
            ops.SUB_OP,  # [1/(pi(a + b)), 10 - (h + 6)]
            ops.SQRT_OP,  # [1/(pi(a + b)), sqrt(10 - (h + 6))]
            3,  # [1/(pi(a + b)), sqrt(10 - (h + 6)), 3]
            ops.SUB_OP,  # [1/(pi(a + b)), 3 - sqrt(10 - (h + 6))]
            ops.DIV_OP,  # pi(a + b)(3 - sqrt(10 - (h + 6))) == Ramanujan's First Ellipse Approximation
        ]
    ),  # test: 17.315086733143538, PID: 4963
)

APPROXIMATES.register(
    "First",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            math.pi,
            6,
            ops.EXP_OP,
            math.pi,
            ops.DIV_OP,
            EllipseProperties.h,
            7,
            3,
            EllipseProperties.h,
            5,
            6,
            ops.DIV_OP,
            9,
            ops.SUB_OP,
            ops.SUB_OP,
            ops.MUL_OP,
            ops.EXP_OP,
            ops.EXP_OP,
            ops.EXP_OP,
            ops.MUL_OP,
        ]
    ),  # test: 909.1790136
)

APPROXIMATES.register(
    "Second",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            2,
            EllipseProperties.h,
            ops.DIV_OP,
            1,
            3,
            ops.INV_OP,
            8,
            9,
            EllipseProperties.h,
            2,
            2,
            ops.DIV_OP,
            ops.SUB_OP,
            ops.ADD_OP,
            ops.DIV_OP,
            ops.MUL_OP,
            ops.SQRT_OP,
            ops.ADD_OP,
            ops.EXP_OP,
            ops.MUL_OP,
        ]
    ),  # test: 814.3767363
)

APPROXIMATES.register(
    "Third",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            2,
            EllipseProperties.h,
            ops.DIV_OP,
            1,
            3,
            ops.INV_OP,
            8,
            6,
            1,
            6,
            EllipseProperties.h,
            ops.ADD_OP,
            ops.INV_OP,
            ops.ADD_OP,
            ops.EXP_OP,
            ops.DIV_OP,
            ops.ADD_OP,
            ops.ADD_OP,
            ops.EXP_OP,
            ops.MUL_OP,
        ]
    ),  # test: 777.5604136
)

APPROXIMATES.register(
    "Fourth",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            7,
            EllipseProperties.h,
            ops.ADD_OP,
            7,
            9,
            8,
            4,
            ops.SQRT_OP,
            8,
            ops.SUB_OP,
            ops.DIV_OP,
            ops.SQRT_OP,
            EllipseProperties.h,
            ops.MUL_OP,
            ops.DIV_OP,
            3,
            ops.EXP_OP,
            ops.DIV_OP,
            ops.MUL_OP,
            ops.MUL_OP,
        ]
    ),  # test: 778.9895021
)

APPROXIMATES.register(
    "Fifth",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            ops.INV_OP,
            EllipseProperties.h,
            8,
            4,
            ops.EXP_OP,
            ops.SQRT_OP,
            ops.INV_OP,
            8,
            10,
            ops.MUL_OP,
            ops.SUB_OP,
            EllipseProperties.h,
            ops.DIV_OP,
            6,
            ops.SQRT_OP,
            math.pi,
            ops.DIV_OP,
            ops.SUB_OP,
            ops.EXP_OP,
            ops.DIV_OP,
        ]
    ),  # test: 767.8231809
)

APPROXIMATES.register(
    "Seventh",
    Calculator(
        [
            math.pi,
            EllipseProperties.a,
            EllipseProperties.b,
            ops.ADD_OP,
            ops.MUL_OP,
            ops.INV_OP,
            EllipseProperties.h,
            8,
            4,
            ops.EXP_OP,
            ops.SQRT_OP,
            ops.INV_OP,
            8,
            10,
            ops.MUL_OP,
            ops.ADD_OP,
            EllipseProperties.h,
            ops.SQRT_OP,
            ops.DIV_OP,
            7,
            9,
            ops.DIV_OP,
            ops.SUB_OP,
            ops.EXP_OP,
            ops.DIV_OP,
        ]
    ),  # test: 1318.637151
)


if __name__ == "__main__":
    from utils import percent_error

    e = EllipseProperties(20, 1)
    print(e.circumference(20))

    def test_stack(name, calc, ellipse):
        calc_perimeter = calc.calculate(ellipse)
        print(
            f"{name}: {calc.to_latex()}, {round(calc_perimeter, 3)}, {round(percent_error(ellipse.circumference(30), calc_perimeter), 3)}%"
        )

    TEST_ELLIPSE = EllipseProperties(20, 5)

    TESTS = APPROXIMATES.getAll()
    for name, calc in TESTS.items():
        test_stack(name, calc, TEST_ELLIPSE)
    print("\n\n\n")
