from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SleepEvent:
    value: int
    original_index: int
    release_time: float


def generate_values(count: int, max_value: int, seed: int | None = None) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(1, max_value) for _ in range(count)]


def build_sleep_sort_schedule(values: list[int], unit_seconds: float) -> list[SleepEvent]:
    ordered = sorted(enumerate(values), key=lambda item: (item[1], item[0]))
    return [
        SleepEvent(value=value, original_index=index, release_time=value * unit_seconds)
        for index, value in ordered
    ]
