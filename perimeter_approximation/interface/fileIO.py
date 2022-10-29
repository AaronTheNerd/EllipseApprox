import datetime
import os

from configs import CONFIGS

from interface.event import Event, EventContext
from interface.interface import Interface
from interface.process_safety import process_safe


@process_safe
class FileIO(Interface):
    activated_events: dict[Event, bool] = {
        Event[key]: val for key, val in CONFIGS.interface.fileio.events.__dict__.items()
    }

    def __init__(self) -> None:
        self.filename = datetime.datetime.now().strftime("output/%m-%d-%Y.%H%M%S.py")
        with open(self.filename, "a+") as file_out:
            file_out.writelines(
                [
                    '"""AUTOMATICALLY GENERATED PYTHON FILE\n\n',
                    "Written by Aaron Barge\n",
                    '"""\n\n\n',
                    "from calculator.calculator import Calculator\n",
                    "import calculator.operators as ops\n",
                    "from ellipse import EllipseProperties\n\n\n",
                ]
            )

    def program_started(self, ctx: EventContext) -> None:
        pass

    def approx_tested(self, ctx: EventContext) -> None:
        pass

    def approx_submitted(self, ctx: EventContext) -> None:
        with open(self.filename, "a+") as outfile:
            test_num = ctx.metadata.post_counts[Event.APPROX_SUBMITTED].value
            outfile.write(
                f"TEST_{test_num} = {ctx.calc} # test: {ctx.test_result}, PID: {os.getpid()}\n"
            )

    def error(self, ctx: EventContext) -> None:
        pass

    def program_finished(self, ctx: EventContext) -> None:
        pass