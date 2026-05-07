from __future__ import annotations

import argparse
import importlib
import sys

DEMOS = {
    "sleep-sort": "algoritmos_curiosos.sleep_sort.main",
    "floyd": "algoritmos_curiosos.floyd_cycle.main",
    "fast-inverse-sqrt": "algoritmos_curiosos.fast_inverse_sqrt.main",
    "bogosort": "algoritmos_curiosos.bogosort.main",
    "maze": "algoritmos_curiosos.maze_generation.main",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lanzador de demos interactivos de algoritmos curiosos."
    )
    parser.add_argument("demo", nargs="?", choices=sorted(DEMOS))
    parser.add_argument("extra", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if not args.demo:
        print("Demos disponibles:")
        for name in sorted(DEMOS):
            print(f"  - {name}")
        print("\nEjemplo: uv run algoritmos-curiosos sleep-sort")
        return

    module = importlib.import_module(DEMOS[args.demo])
    sys.argv = [sys.argv[0], *args.extra]
    module.main()
