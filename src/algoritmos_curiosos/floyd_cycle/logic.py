from __future__ import annotations

from dataclasses import dataclass


def build_cycle_next_indices(tail_length: int, cycle_length: int) -> list[int]:
    total_nodes = tail_length + cycle_length
    next_indices = [0] * total_nodes
    for index in range(total_nodes - 1):
        next_indices[index] = index + 1
    next_indices[-1] = tail_length
    return next_indices


def advance(next_indices: list[int], current: int, steps: int = 1) -> int:
    for _ in range(steps):
        current = next_indices[current]
    return current


@dataclass(frozen=True)
class FloydResult:
    meeting_index: int
    mu: int
    lam: int
    steps_until_meeting: int


def floyd_detect(next_indices: list[int], start: int = 0) -> FloydResult:
    tortoise = advance(next_indices, start, 1)
    hare = advance(next_indices, start, 2)
    steps = 1
    while tortoise != hare:
        tortoise = advance(next_indices, tortoise, 1)
        hare = advance(next_indices, hare, 2)
        steps += 1

    mu = 0
    tortoise = start
    while tortoise != hare:
        tortoise = advance(next_indices, tortoise, 1)
        hare = advance(next_indices, hare, 1)
        mu += 1

    lam = 1
    hare = advance(next_indices, tortoise, 1)
    while tortoise != hare:
        hare = advance(next_indices, hare, 1)
        lam += 1

    return FloydResult(meeting_index=tortoise, mu=mu, lam=lam, steps_until_meeting=steps)
