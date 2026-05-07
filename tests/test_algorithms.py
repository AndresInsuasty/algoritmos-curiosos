from __future__ import annotations

from algoritmos_curiosos.bogosort.logic import is_sorted, quantum_bogosort
from algoritmos_curiosos.fast_inverse_sqrt.logic import exact_inverse_sqrt, fast_inverse_sqrt
from algoritmos_curiosos.floyd_cycle.logic import build_cycle_next_indices, floyd_detect
from algoritmos_curiosos.maze_generation.logic import kruskal_carving_order, prim_carving_order, solve_path
from algoritmos_curiosos.sleep_sort.logic import build_sleep_sort_schedule


def test_sleep_sort_schedule_orders_values() -> None:
    schedule = build_sleep_sort_schedule([4, 1, 3, 1], 0.2)
    assert [event.value for event in schedule] == [1, 1, 3, 4]
    assert [event.original_index for event in schedule] == [1, 3, 2, 0]


def test_floyd_detect_returns_tail_and_cycle_lengths() -> None:
    next_indices = build_cycle_next_indices(tail_length=4, cycle_length=6)
    result = floyd_detect(next_indices)
    assert result.mu == 4
    assert result.lam == 6


def test_fast_inverse_sqrt_is_close_to_exact_value() -> None:
    number = 81.0
    approximate = fast_inverse_sqrt(number, iterations=1)
    exact = exact_inverse_sqrt(number)
    assert exact == 1 / 9
    assert abs(approximate - exact) / exact < 0.01


def test_quantum_bogosort_collapses_to_sorted_values() -> None:
    assert not is_sorted([3, 1, 2])
    assert quantum_bogosort([3, 1, 2]) == [1, 2, 3]


def test_maze_algorithms_generate_connected_perfect_mazes() -> None:
    rows = 5
    cols = 6
    for generator in (prim_carving_order, kruskal_carving_order):
        carvings = generator(rows, cols, seed=4)
        assert len(carvings) == rows * cols - 1
        path = solve_path(rows, cols, carvings)
        assert path[0] == (0, 0)
        assert path[-1] == (rows - 1, cols - 1)
