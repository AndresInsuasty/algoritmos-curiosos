from __future__ import annotations

import random
from collections import deque

Cell = tuple[int, int]
Edge = tuple[Cell, Cell]


def grid_neighbors(rows: int, cols: int, cell: Cell) -> list[Cell]:
    row, col = cell
    neighbors: list[Cell] = []
    for d_row, d_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_row = row + d_row
        next_col = col + d_col
        if 0 <= next_row < rows and 0 <= next_col < cols:
            neighbors.append((next_row, next_col))
    return neighbors


def normalized_edge(start: Cell, end: Cell) -> Edge:
    return (start, end) if start <= end else (end, start)


def prim_carving_order(rows: int, cols: int, seed: int | None = None) -> list[Edge]:
    rng = random.Random(seed)
    start = (rng.randrange(rows), rng.randrange(cols))
    visited = {start}
    frontier = [normalized_edge(start, neighbor) for neighbor in grid_neighbors(rows, cols, start)]
    carvings: list[Edge] = []

    while frontier:
        edge = frontier.pop(rng.randrange(len(frontier)))
        first, second = edge
        if first in visited and second in visited:
            continue
        new_cell = second if first in visited else first
        old_cell = first if new_cell == second else second
        carvings.append(normalized_edge(old_cell, new_cell))
        visited.add(new_cell)
        for neighbor in grid_neighbors(rows, cols, new_cell):
            if neighbor not in visited:
                frontier.append(normalized_edge(new_cell, neighbor))

    return carvings


class DisjointSet:
    def __init__(self, cells: list[Cell]) -> None:
        self.parent = {cell: cell for cell in cells}
        self.rank = {cell: 0 for cell in cells}

    def find(self, item: Cell) -> Cell:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: Cell, right: Cell) -> bool:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return False
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1
        return True


def kruskal_carving_order(rows: int, cols: int, seed: int | None = None) -> list[Edge]:
    rng = random.Random(seed)
    cells = [(row, col) for row in range(rows) for col in range(cols)]
    disjoint = DisjointSet(cells)
    edges = [
        normalized_edge((row, col), neighbor)
        for row in range(rows)
        for col in range(cols)
        for neighbor in grid_neighbors(rows, cols, (row, col))
        if (row, col) < neighbor
    ]
    rng.shuffle(edges)

    carvings: list[Edge] = []
    for start, end in edges:
        if disjoint.union(start, end):
            carvings.append((start, end))

    return carvings


def build_passages(carvings: list[Edge]) -> dict[Cell, set[Cell]]:
    passages: dict[Cell, set[Cell]] = {}
    for start, end in carvings:
        passages.setdefault(start, set()).add(end)
        passages.setdefault(end, set()).add(start)
    return passages


def solve_path(rows: int, cols: int, carvings: list[Edge]) -> list[Cell]:
    passages = build_passages(carvings)
    start = (0, 0)
    goal = (rows - 1, cols - 1)
    queue = deque([start])
    previous: dict[Cell, Cell | None] = {start: None}

    while queue:
        cell = queue.popleft()
        if cell == goal:
            break
        for neighbor in passages.get(cell, set()):
            if neighbor not in previous:
                previous[neighbor] = cell
                queue.append(neighbor)

    path: list[Cell] = []
    current: Cell | None = goal
    while current is not None:
        path.append(current)
        current = previous.get(current)
    return list(reversed(path))
