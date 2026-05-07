from __future__ import annotations

import random


def is_sorted(values: list[int]) -> bool:
    return all(left <= right for left, right in zip(values, values[1:]))


def bogosort_step(values: list[int], rng: random.Random) -> list[int]:
    shuffled = values[:]
    rng.shuffle(shuffled)
    return shuffled


def quantum_bogosort(values: list[int]) -> list[int]:
    return sorted(values)
