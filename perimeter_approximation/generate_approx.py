import ctypes
import multiprocessing as mproc
import random
from typing import Any

import numpy as np

import calculator.operators as ops
from calculator.calculator import Calculator
from calculator.constants import Constants
from calculator.error import CalculatorError, OperatorError
from configs import CONFIGS
from interface.event import Event, EventContext
from interface.event_handler import HANDLER
from test_approx import test_approximation
from utils import all, divide_list


class ApproxGenerator:
    def __init__(self, calc: Calculator, calc_elems: list[Any]) -> None:
        self.calc = calc
        self.calc_elems = calc_elems
        self.curr_best = mproc.Value(ctypes.c_float, CONFIGS.approx.max_test_score)
        self.failed_due_to_error = False
        self.failed_index = -1

    def _gen_approx_helper(self, valid_calc_elems: list[Any]) -> None:
        for elem in valid_calc_elems:
            self.calc.append(elem)
            self._generate_approximations()
            self.calc.pop()

    def _generate_approximations(self, first_run: bool = False) -> None:
        calc_validate = self.calc.validate()
        ctx = EventContext(calc=self.calc)
        test_result = None

        if self.failed_due_to_error:

            if self.failed_index == -1 or len(self.calc.stack) < self.failed_index:
                try:
                    test_result = test_approximation(self.calc, max_value=self.curr_best.value)
                except CalculatorError:
                    self.failed_due_to_error = False
                    self.failed_index = -1
                except Exception:
                    return
            else:
                return

        elif calc_validate == 1:

            HANDLER.post(Event.APPROX_TESTED, ctx)
            if test_result is None:
                try:
                    test_result = test_approximation(self.calc, max_value=self.curr_best.value)
                except OperatorError as e:
                    ctx.err = e
                    HANDLER.post(Event.ERROR, ctx)
                    self.failed_due_to_error = True
                    self.failed_index = e.failed_index
                    return
                except Exception as e:
                    ctx.err = e
                    HANDLER.post(Event.ERROR, ctx)
                    self.failed_due_to_error = True
                    self.failed_index = -1
                    return

            with self.curr_best.get_lock():
                if test_result < self.curr_best.value:
                    ctx.test_result = test_result
                    HANDLER.post(Event.APPROX_SUBMITTED, ctx)
                    if CONFIGS.approx.save_current_best:
                        self.curr_best.value = test_result
        
        if (
            len(self.calc.stack) >= CONFIGS.approx.max_stack_size
            or CONFIGS.approx.max_stack_size - len(self.calc.stack) < calc_validate - 1
        ):
            return

        filters = []

        # Filter any operator which requires too many arguments
        filters.append(lambda x: not isinstance(x, ops.Operator) or x.args <= calc_validate)

        # If the number stack elements left to have is equal to the number of binary operators needed to complete the formula,
        # filter non binary operators
        if CONFIGS.approx.max_stack_size - len(self.calc.stack) == calc_validate - 1:
            filters.append(lambda x: isinstance(x, ops.Operator) and x.args > 1)

        if len(self.calc.stack) > 0:
            a = self.calc.stack[-1]
            if CONFIGS.approx.filters.primitive_subformulas and Constants.primitive_constant(a):
                filters.append(lambda x: not isinstance(x, ops.Operator) or x.args != 1)

        if len(self.calc.stack) > 1:
            a = self.calc.stack[-2]
            b = self.calc.stack[-1]
            if (
                CONFIGS.approx.filters.primitive_subformulas
                and Constants.primitive_constant(a)
                and Constants.primitive_constant(b)
            ):
                filters.append(lambda x: not isinstance(x, ops.Operator) or x.args != 2)

            filters.append(lambda x: not isinstance(x, ops.Operator) or not x.constrain(a, b))

        valid_calc_elems = list(filter(all(filters), self.calc_elems))
        random.shuffle(valid_calc_elems)
        
        if first_run and CONFIGS.subprocess_count > 1:
            threads = [
                mproc.Process(target=self._gen_approx_helper, args=(valid_calc_elems_basket,))
                for valid_calc_elems_basket in divide_list(
                    valid_calc_elems, CONFIGS.subprocess_count
                )
            ]
            print(f"PROCESSES: {threads}")
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            return
        
        for elem in valid_calc_elems:
            self.calc.append(elem)
            self._generate_approximations()
            self.calc.pop()

    def run(self):
        self._generate_approximations(True)
