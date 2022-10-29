"""A module which handles the calling of events.

Written by Aaron Barge
Copyright 2022
"""


from configs import CONFIGS

from interface.CLI import CLI
from interface.event import Event, EventContext, EventMetadata
from interface.fileIO import FileIO
from interface.email import Email
from interface.interface import Interface
from interface.process_safety import process_safe


@process_safe
class EventHandler:
    """A class for handling the calling of events."""

    def __init__(self) -> None:
        self.metadata = EventMetadata()
        self.subscribers: list[Interface] = []

    def subscribe(self, interface: Interface) -> None:
        self.subscribers += [interface]

    def post(self, event: Event, ctx: EventContext = EventContext()) -> None:
        # Update metadata
        with self.metadata.post_counts[event].get_lock():
            self.metadata.post_counts[event].value += 1
        if event == Event.APPROX_SUBMITTED and ctx.calc is not None:
            self.metadata.best_approx = ctx.calc

        # Attach metadata to context
        ctx.metadata = self.metadata

        # Notify subscribers
        for subscriber in self.subscribers:
            subscriber.run(event, ctx)

    def get_metadata(self) -> EventMetadata:
        return self.metadata


HANDLER = EventHandler()
if CONFIGS.interface.cli.enabled:
    HANDLER.subscribe(CLI(**CONFIGS.interface.cli.kwargs))
if CONFIGS.interface.fileio.enabled:
    HANDLER.subscribe(FileIO(**CONFIGS.interface.fileio.kwargs))
if CONFIGS.interface.email.enabled:
    HANDLER.subscribe(Email(**CONFIGS.interface.email.kwargs))
