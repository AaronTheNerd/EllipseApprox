"""A module for generating the constants and inputs needed for the calculator.

Written by Aaron Barge
Copyright 2022
"""

import math
from typing import Any

import numpy as np
from configs import ConstantsConfigs
from ellipse import EllipseProperties


class Constants:
    def __init__(self, configs: ConstantsConfigs):
        self.constants = [
            x.item() for x in np.arange(configs.min_value, configs.max_value, configs.step)
        ]
        self.constants += [EllipseProperties.a, EllipseProperties.b]
        if configs.include_pi:
            self.constants += [math.pi]
        if configs.include_ellipse_properties:
            self.constants += [EllipseProperties.c, EllipseProperties.e, EllipseProperties.h]

    def get_constants(self) -> list[Any]:
        return self.constants

    @staticmethod
    def primitive_constant(value):
        return type(value) in [int, float] and value != math.pi
