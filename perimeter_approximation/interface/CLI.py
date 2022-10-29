import time

from configs import CONFIGS

from interface.event import Event, EventContext
from interface.interface import Interface
from interface.process_safety import process_safe


@process_safe
class CLI(Interface):
    activated_events: dict[Event, bool] = {
        Event[key]: val for key, val in CONFIGS.interface.cli.events.__dict__.items()
    }

    def __init__(self) -> None:
        pass

    def program_started(self, ctx: EventContext) -> None:
        self.start = time.time()

    def approx_tested(self, ctx: EventContext) -> None:
        self.approx_submitted(ctx)

    def approx_submitted(self, ctx: EventContext) -> None:
        elapsed_time = time.time() - self.start
        submitted = ctx.metadata.post_counts[Event.APPROX_SUBMITTED].value
        tested = ctx.metadata.post_counts[Event.APPROX_TESTED].value
        error = ctx.metadata.post_counts[Event.ERROR].value
        print(
            f"Generated {submitted:,}/{tested:,} approximations @ {round(tested / elapsed_time):,} approx/s, {round(error / (tested if tested != 0 else 1) * 100, 1)}% error{' ' * 10}",
            end="\r",
        )

    def error(self, ctx: EventContext) -> None:
        print(f"[ERROR#{ctx.metadata.post_counts[Event.ERROR].value}] {ctx.err}{' ' * 40}")
        self.approx_submitted(ctx)

    def program_finished(self, ctx: EventContext) -> None:
        print(f"\nProgram finished after: {round(time.time() - self.start)} seconds")
