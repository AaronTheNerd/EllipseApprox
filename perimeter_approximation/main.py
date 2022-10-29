# Written by Aaron Barge
# Copyright 2022
import math
import random

import calculator.operators as ops
from calculator.calculator import Calculator
from calculator.constants import Constants
from configs import CONFIGS
from ellipse import EllipseProperties
from generate_approx import ApproxGenerator
from interface.event import Event, EventContext
from interface.event_handler import HANDLER, EventHandler


def main():
    HANDLER.post(Event.PROGRAM_STARTED)
    calc_elems = []
    calc_elems += [
        ops.ADD_OP,
        ops.SUB_OP,
        ops.MUL_OP,
        ops.DIV_OP,
        ops.EXP_OP,
        ops.SQRT_OP,
        ops.NEG_OP,
        ops.INV_OP,
    ]
    calc_elems += Constants(CONFIGS.approx.constants).get_constants()
    random.seed(CONFIGS.seed)
    calc = Calculator([eval(x) for x in CONFIGS.approx.calc_prefix])
    gen = ApproxGenerator(calc, calc_elems)
    gen.run()
    HANDLER.post(Event.PROGRAM_FINISHED)


if __name__ == "__main__":
    main()
