import numpy as np

from configs import CONFIGS, DataGenerationConfigs
from ellipse import EllipseProperties


def _generation_helper(
    configs: DataGenerationConfigs, dim: int, data: list[tuple[float, ...]]
) -> list[tuple[float, ...]]:
    if dim == 0:
        return [x + (EllipseProperties(*x).circumference(configs.precision),) for x in data]
    new_data = [
        x + (i,)
        for x in data
        for i in np.arange(configs.min_value, configs.max_value, configs.step)
    ]
    return _generation_helper(configs, dim - 1, new_data)


def generate(configs: DataGenerationConfigs) -> list[tuple[float, ...]]:
    if configs.dimensions < 1:
        raise Exception("DataGeneration's Dimension must be at least 1")
    default_data = [(x,) for x in np.arange(configs.min_value, configs.max_value, configs.step)]
    return _generation_helper(configs, configs.dimensions - 1, default_data)


TEST_DATA = generate(CONFIGS.test.data)
PLOT_DATA = generate(CONFIGS.plot.data)


if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(width=80, indent=2, compact=False)
    print("Plot Data: ", end="")
    pp.pprint(PLOT_DATA)
    print("\n\n\nTest Data: ", end="")
    pp.pprint(TEST_DATA)
    print("\n\n\n")
