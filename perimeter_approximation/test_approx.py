from typing import Optional

import numpy as np  # type: ignore
from calculator.calculator import Calculator
from configs import CONFIGS
from data import TEST_DATA
from ellipse import EllipseProperties


def test_approximation(calc: Calculator, test_data: list[tuple[float, ...]] = TEST_DATA, max_value: Optional[float] = CONFIGS.approx.max_test_score) -> float:
    total_square_error = 0.0
    for *axises, actual in test_data:
        ellipse = EllipseProperties(*axises)
        calc_perimeter = calc.calculate(ellipse)
        total_square_error += 100 * abs(calc_perimeter - actual)
        if max_value is not None and max_value < total_square_error:
            return max_value
    if not isinstance(total_square_error, (int, float, np.floating)):
        raise Exception("Invalid test result")
    return total_square_error


def test_for_error(calc: Calculator, *args, **kwargs) -> None:
    calc_perimeter = calc.calculate(*args, **kwargs)
    if not isinstance(calc_perimeter, (int, float, np.floating)):
        raise Exception("Invalid test result")


if __name__ == "__main__":
    from approximates import APPROXIMATES

    def test_stack(name, calc):
        total_error = test_approximation(calc)
        print(f"{name}: {round(total_error, 3)}")

    TESTS = APPROXIMATES.getAll()
    for name, calc in TESTS.items():
        test_stack(name, calc)
    print("\n\n\n")
