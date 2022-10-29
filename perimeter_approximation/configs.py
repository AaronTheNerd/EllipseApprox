"""A module containing the configs for the project.

Written by Aaron Barge
Copyright 2022
"""

import json
import os
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, Optional, TypeVar

import utils


@dataclass(frozen=True)
class ConstantsConfigs:
    """Represents the configs needed to define which constants can be included in the approximation."""

    min_value: float
    max_value: float
    step: float
    include_pi: bool
    include_ellipse_properties: bool


@dataclass(frozen=True)
class FilterConfigs:
    primitive_subformulas: bool = field(default=True)


@dataclass(frozen=True)
class ApproximationConfigs:
    """Represents the configs needed for ellipse approximation generation."""

    max_stack_size: int
    max_test_score: float
    save_current_best: bool
    calc_prefix: list[str]
    constants: ConstantsConfigs
    filters: FilterConfigs


@dataclass(frozen=True)
class DataGenerationConfigs:
    dimensions: int
    min_value: float
    max_value: float
    step: float
    precision: int


@dataclass(frozen=True)
class PlotConfigs:
    data: DataGenerationConfigs
    style_sheet: str
    image_filename: str
    title: str
    xlabel: str
    ylabel: str


@dataclass(frozen=True)
class TestConfigs:
    data: DataGenerationConfigs


@dataclass(frozen=True)
class EnabledEventsConfigs:
    PROGRAM_STARTED: bool = field(default=False)
    APPROX_TESTED: bool = field(default=False)
    APPROX_SUBMITTED: bool = field(default=False)
    ERROR: bool = field(default=False)
    PROGRAM_FINISHED: bool = field(default=False)


@dataclass(frozen=True)
class InterfaceEnabledConfigs:
    enabled: bool
    events: EnabledEventsConfigs = field(default_factory=EnabledEventsConfigs)
    kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InterfaceConfigs:
    cli: InterfaceEnabledConfigs
    fileio: InterfaceEnabledConfigs
    email: InterfaceEnabledConfigs


@dataclass(frozen=True)
class Configs:
    """Represents configs needed for running the program."""

    subprocess_count: int
    approx: ApproximationConfigs
    plot: PlotConfigs
    test: TestConfigs
    interface: InterfaceConfigs
    seed: int = field(default_factory=utils.seed_factory)


T = TypeVar("T")


def _replaceWithDataclass(raw_configs: dict[str, Any], cls: type[T]) -> T:
    for field in fields(cls):
        if is_dataclass(field.type):
            raw_configs[field.name] = _replaceWithDataclass(raw_configs[field.name], field.type)
    return cls(**raw_configs)


def _getConfigs() -> Configs:
    """Converts configs.json into a python dataclass for code use."""
    abs_path = os.path.abspath(os.path.dirname(__file__))
    raw_configs = {}
    with open(f"{abs_path}/../configs.json") as configs:
        raw_configs = json.load(configs)
    return _replaceWithDataclass(raw_configs, Configs)


CONFIGS = _getConfigs()


if __name__ == "__main__":
    print(CONFIGS)
    print("\n\n\n")
