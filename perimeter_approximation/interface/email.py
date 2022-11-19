"""A module which facilitates sending emails.

Written by Aaron Barge
Copyright 2022
"""


import os
from test_approx import test_approximation
import yagmail # type: ignore
from configs import CONFIGS
from functools import partial
from interface.event import Event, EventContext
from interface.interface import Interface
from interface.process_safety import process_safe

from approximates import APPROXIMATES
from plot import plot


@process_safe
class Email(Interface):

    activated_events: dict[Event, bool] = {
        Event[key]: val for key, val in CONFIGS.interface.email.events.__dict__.items()
    }

    BENCHMARK_BEATEN = """
<html style="color: black;">
    <div>
        <font size="6">New Approximation Found</font>
    </div>
    <br>
    <div>
        <font size="5">Formula:</font>
    </div>
    <div>
        <font size="4">${formula}</font>
    </div>
    <br>
    <div>
        <font size="5">Stack:</font>
    </div>
    <div>
        <font size="4">{stack}</font>
    </div>
    <br>
    <div>
        <font size="5">Has Beaten:</font>
    </div>
    <div>
        <font size="4">{benchmarks}</font>
    </div>
    <br>
    <div>
        <font size="5">Test Result: {test_result}</font>
    </div>
    <br>
    <div>
        <font size="4">Beep-boop, boop-beep</font>
    </div>
</html>
"""

    OVERKILL = """
<html style="color: black;">
    <div>
        <font size="6">New Approximation Found</font>
    </div>
    <br>
    <div>
        <font size="5">Formula:</font>
    </div>
    <div>
        <font size="4">${formula}</font>
    </div>
    <br>
    <div>
        <font size="5">Stack:</font>
    </div>
    <div>
        <font size="4">{stack}</font>
    </div>
    <br>
    <div>
        <font size="5">Test Result: {test_result}</font>
    </div>
    <br>
    <div>
        <font size="4">Beep-boop, boop-beep</font>
    </div>
</html>
"""

    def __init__(
        self, dev_email: str, dev_password: str, recipient_email: str, benchmarks: list[str]
    ) -> None:
        self.yag = yagmail.SMTP(dev_email, dev_password)
        self.recipient_email = recipient_email
        self.benchmarks = benchmarks

    def send_email(self, subject: str, message: str, attachments: list[str]) -> None:
        self.yag.send(self.recipient_email, subject, [message], attachments=attachments)

    @staticmethod
    def filter_benchmarks(test_result: float, id: str):
        approx = APPROXIMATES[id]
        return approx is not None and test_approximation(approx, max_value=None) >= test_result

    def program_started(self, ctx: EventContext) -> None:
        pass

    def approx_tested(self, ctx: EventContext) -> None:
        pass

    def approx_submitted(self, ctx: EventContext) -> None:
        if ctx.calc is None or ctx.test_result is None:
            return

        filtered_benchmarks = list(
            filter(partial(self.filter_benchmarks, ctx.test_result), self.benchmarks)
        )
        
        if len(filtered_benchmarks) == 0 and len(self.benchmarks) > 0:
            return
        approxes = {x : approx for x in filtered_benchmarks if (approx := APPROXIMATES[x]) is not None}
        approxes["Generated"] = ctx.calc
        plot(approxes)
        if len(filtered_benchmarks) > 0:
            for beaten in filtered_benchmarks:
                self.benchmarks.remove(beaten)
            self.send_email(
                "[AUTOMATED] Benchmark Beaten",
                self.BENCHMARK_BEATEN.format(
                    stack=str(ctx.calc),
                    formula=ctx.calc.to_latex(),
                    benchmarks=filtered_benchmarks,
                    test_result=ctx.test_result,
                ),
                [CONFIGS.plot.image_filename]
            )
        elif len(self.benchmarks) == 0:
            self.send_email(
                "[AUTOMATED] Formula Overkill",
                self.OVERKILL.format(
                    stack=ctx.calc.stack,
                    test_result=ctx.test_result,
                ),
                [CONFIGS.plot.image_filename]
            )

    def error(self, ctx: EventContext) -> None:
        pass

    def program_finished(self, ctx: EventContext) -> None:
        pass
