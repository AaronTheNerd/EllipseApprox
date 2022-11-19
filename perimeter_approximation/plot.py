import matplotlib.pyplot as plt

import utils
from calculator.calculator import Calculator
from configs import CONFIGS
from data import PLOT_DATA
from ellipse import EllipseProperties


def plot(approximations: dict[str, Calculator]) -> None:
    plt.style.use(["dark_background", CONFIGS.plot.style_sheet])
    fig, ax = plt.subplots()
    xs = [x for x, *_ in PLOT_DATA]
    max_y = 0
    for label, approx in approximations.items():
        ys = [
            utils.percent_error(actual, approx.calculate(EllipseProperties(a)))
            for a, actual in PLOT_DATA
        ]
        curr_max_y = max(ys)
        if curr_max_y > max_y:
            max_y = curr_max_y
        ax.plot(xs, ys, label=label)
    ax.set_xlim((CONFIGS.plot.data.min_value, CONFIGS.plot.data.max_value))
    ax.set_ylim(ymin=0)
    ax.set_xlabel(CONFIGS.plot.xlabel)
    ax.set_ylabel(CONFIGS.plot.ylabel)
    ax.set_title(CONFIGS.plot.title)
    ax.legend()
    plt.savefig(CONFIGS.plot.image_filename)


if __name__ == "__main__":
    from approximates import APPROXIMATES
    approxes = ["Seventh", "Ramanujan1"]
    plot({x: approx for x in approxes if (approx := APPROXIMATES[x]) is not None})
    print("\n\n\n")
