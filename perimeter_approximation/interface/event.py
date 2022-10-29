"""A module containing everything for sending events.

Written by Aaron Barge
Copyright 2022
"""


import ctypes
import multiprocessing as mproc
from dataclasses import dataclass, field
from enum import Enum
from multiprocessing.managers import BaseManager
from multiprocessing.sharedctypes import SynchronizedBase
from typing import Optional

from calculator.calculator import Calculator


class Event(Enum):
    PROGRAM_STARTED = "PROGRAM_STARTED"
    APPROX_TESTED = "APPROX_TESTED"
    APPROX_SUBMITTED = "APPROX_SUBMITTED"
    ERROR = "ERROR"
    PROGRAM_FINISHED = "PROGRAM_FINISHED"


def _init_post_counts():
    return {x: mproc.Value(ctypes.c_uint64, 0) for x in list(Event)}


class MetadataManager(BaseManager):
    pass


class EventMetadata:
    def __init__(self):
        self.post_counts: dict[Event, SynchronizedBase[ctypes.c_uint64]] = _init_post_counts()
        MetadataManager.register('Calculator', Calculator)
        self._manager: MetadataManager = MetadataManager()
        self._manager.start()
        self.best_approx: Calculator = self._manager.Calculator()

    def __del__(self):
        self._manager.shutdown()


@dataclass
class EventContext:
    calc: Optional[Calculator] = field(default=None)
    test_result: Optional[float] = field(default=None)
    err: Optional[Exception] = field(default=None)
    metadata: EventMetadata = field(init=False)

