from abc import ABC, abstractmethod

from calculator.calculator import Calculator

from interface.event import Event, EventMetadata, EventContext


class Interface(ABC):
    activated_events: dict[Event, bool] = {}

    def run(self, event: Event, ctx: EventContext) -> None:
        if not self.activated_events[event]:
            return
        match event:
            case Event.PROGRAM_STARTED:
                return self.program_started(ctx)
            case Event.APPROX_TESTED:
                return self.approx_tested(ctx)
            case Event.APPROX_SUBMITTED:
                return self.approx_submitted(ctx)
            case Event.ERROR:
                return self.error(ctx)
            case Event.PROGRAM_FINISHED:
                return self.program_finished(ctx)
            case _:
                raise Exception(f"Unknown event: {event}")

    @abstractmethod
    def program_started(self, ctx: EventContext) -> None:
        ...

    @abstractmethod
    def approx_tested(self, ctx: EventContext) -> None:
        ...

    @abstractmethod
    def approx_submitted(self, ctx: EventContext) -> None:
        ...

    @abstractmethod
    def error(self, ctx: EventContext) -> None:
        ...

    @abstractmethod
    def program_finished(self, ctx: EventContext) -> None:
        ...
