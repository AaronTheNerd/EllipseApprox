import matplotlib.pyplot as plt

import utils
from calculator.calculator import Calculator
from configs import CONFIGS
from data import PLOT_DATA
from ellipse import EllipseProperties


def plot(approximations: list[Calculator]) -> None:
    plt.style.use(["dark_background", CONFIGS.plot.style_sheet])
    fig, ax = plt.subplots()
    xs = [x for x, *_ in PLOT_DATA]
    max_y = 0
    for approx in approximations:
        ys = [
            utils.percent_error(actual, approx.calculate(EllipseProperties(a)))
            for a, actual in PLOT_DATA
        ]
        curr_max_y = max(ys)
        if curr_max_y > max_y:
            max_y = curr_max_y
        ax.plot(xs, ys)
    ax.set_xlim((CONFIGS.plot.data.min_value, CONFIGS.plot.data.max_value))
    ax.set_ylim(ymin=0)
    ax.set_xlabel(CONFIGS.plot.xlabel)
    ax.set_ylabel(CONFIGS.plot.ylabel)
    ax.set_title(CONFIGS.plot.title)
    plt.savefig(CONFIGS.plot.image_filename)


if __name__ == "__main__":
    from approximates import APPROXIMATES

    plot(
        [
            x
            for x in [APPROXIMATES["Sixth"], APPROXIMATES["Ramanujan1"]]
            if x is not None
        ]
    )
    print("\n\n\n")
