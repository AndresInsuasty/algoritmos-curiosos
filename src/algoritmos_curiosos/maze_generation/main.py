from __future__ import annotations

import random

import pygame

from algoritmos_curiosos.common import (
    ACCENT,
    BACKGROUND,
    DANGER,
    MUTED,
    WARNING,
    Button,
    DemoBase,
    draw_panel,
    draw_text,
    run_demo,
)
from algoritmos_curiosos.maze_generation.logic import (
    Edge,
    build_passages,
    kruskal_carving_order,
    prim_carving_order,
    solve_path,
)


class MazeGenerationDemo(DemoBase):
    title = "Generación de laberintos — Prim y Kruskal"

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.rows = 10
        self.cols = 14
        self.algorithm = "Prim"
        self.speed = 18.0
        self.rng = random.Random(23)
        self.carving_order: list[Edge] = []
        self.current_edges: list[Edge] = []
        self.path: list[tuple[int, int]] = []
        self.progress = 0.0
        self.runner_progress = 0.0
        self.runner_index = 0
        self.running = False
        self._build_buttons()
        self.prepare_generation()

    def _build_buttons(self) -> None:
        y = self.height - 84
        self.buttons = [
            Button("filas −", pygame.Rect(40, y, 90, 42), "rows_down"),
            Button("filas +", pygame.Rect(138, y, 90, 42), "rows_up"),
            Button("cols −", pygame.Rect(254, y, 90, 42), "cols_down"),
            Button("cols +", pygame.Rect(352, y, 90, 42), "cols_up"),
            Button("Algoritmo", pygame.Rect(476, y, 130, 42), "toggle_algorithm"),
            Button("Generar", pygame.Rect(624, y, 130, 42), "run", fill=ACCENT),
            Button("Reset", pygame.Rect(772, y, 130, 42), "reset", fill=DANGER),
        ]

    def prepare_generation(self) -> None:
        seed = self.rng.randint(0, 9999)
        if self.algorithm == "Prim":
            self.carving_order = prim_carving_order(self.rows, self.cols, seed=seed)
        else:
            self.carving_order = kruskal_carving_order(self.rows, self.cols, seed=seed)
        self.current_edges = []
        self.path = []
        self.progress = 0.0
        self.runner_progress = 0.0
        self.runner_index = 0
        self.running = False

    def on_autoplay(self) -> None:
        self.running = True

    def on_button(self, action: str) -> None:
        if action == "rows_down":
            self.rows = max(6, self.rows - 1)
            self.prepare_generation()
        elif action == "rows_up":
            self.rows = min(16, self.rows + 1)
            self.prepare_generation()
        elif action == "cols_down":
            self.cols = max(6, self.cols - 1)
            self.prepare_generation()
        elif action == "cols_up":
            self.cols = min(20, self.cols + 1)
            self.prepare_generation()
        elif action == "toggle_algorithm":
            self.algorithm = "Kruskal" if self.algorithm == "Prim" else "Prim"
            self.prepare_generation()
        elif action == "run":
            self.running = True
        elif action == "reset":
            self.prepare_generation()

    def update(self, dt: float) -> None:
        if self.running and len(self.current_edges) < len(self.carving_order):
            self.progress += dt * self.speed
            while self.progress >= 1 and len(self.current_edges) < len(self.carving_order):
                self.current_edges.append(self.carving_order[len(self.current_edges)])
                self.progress -= 1
            if len(self.current_edges) == len(self.carving_order):
                self.path = solve_path(self.rows, self.cols, self.current_edges)
                self.runner_index = 0
                self.runner_progress = 0.0
        elif self.path:
            self.runner_progress += dt * 3
            while self.runner_progress >= 1 and self.runner_index < len(self.path) - 1:
                self.runner_index += 1
                self.runner_progress -= 1

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        panel = pygame.Rect(28, 24, self.width - 56, 156)
        draw_panel(screen, panel)
        draw_text(screen, "Generación de laberintos", (48, 42), size=32, bold=True)
        draw_text(
            screen,
            f"Algoritmo: {self.algorithm}   Tamaño: {self.rows}×{self.cols}   Pasajes abiertos: {len(self.current_edges)} / {len(self.carving_order)}",
            (48, 84),
            color=MUTED,
        )
        draw_text(
            screen,
            "Al finalizar, el explorador azul recorre la solución desde la entrada hasta la salida.",
            (48, 118),
            color=WARNING,
            size=22,
        )

        board = pygame.Rect(40, 210, self.width - 80, self.height - 320)
        draw_panel(screen, board)
        cell_size = min((board.width - 40) / self.cols, (board.height - 40) / self.rows)
        offset_x = board.x + (board.width - cell_size * self.cols) / 2
        offset_y = board.y + (board.height - cell_size * self.rows) / 2
        passages = build_passages(self.current_edges)

        for row in range(self.rows):
            for col in range(self.cols):
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, (26, 32, 52), rect)
                cell = (row, col)
                neighbors = passages.get(cell, set())
                if (row - 1, col) not in neighbors:
                    pygame.draw.line(screen, (235, 239, 255), (x, y), (x + cell_size, y), 2)
                if (row, col - 1) not in neighbors:
                    pygame.draw.line(screen, (235, 239, 255), (x, y), (x, y + cell_size), 2)
                if (row + 1, col) not in neighbors:
                    pygame.draw.line(
                        screen,
                        (235, 239, 255),
                        (x, y + cell_size),
                        (x + cell_size, y + cell_size),
                        2,
                    )
                if (row, col + 1) not in neighbors:
                    pygame.draw.line(
                        screen,
                        (235, 239, 255),
                        (x + cell_size, y),
                        (x + cell_size, y + cell_size),
                        2,
                    )

        if self.path:
            for cell in self.path:
                row, col = cell
                x = offset_x + col * cell_size + cell_size / 2
                y = offset_y + row * cell_size + cell_size / 2
                pygame.draw.circle(screen, (90, 110, 170), (int(x), int(y)), max(3, int(cell_size * 0.12)))
            runner_cell = self.path[self.runner_index]
            row, col = runner_cell
            x = offset_x + col * cell_size + cell_size / 2
            y = offset_y + row * cell_size + cell_size / 2
            pygame.draw.circle(screen, ACCENT, (int(x), int(y)), max(6, int(cell_size * 0.22)))

        pygame.draw.rect(
            screen,
            ACCENT,
            pygame.Rect(offset_x + 4, offset_y + 4, cell_size - 8, cell_size - 8),
            border_radius=6,
            width=2,
        )
        pygame.draw.rect(
            screen,
            WARNING,
            pygame.Rect(
                offset_x + (self.cols - 1) * cell_size + 4,
                offset_y + (self.rows - 1) * cell_size + 4,
                cell_size - 8,
                cell_size - 8,
            ),
            border_radius=6,
            width=2,
        )

        for button in self.buttons:
            button.draw(screen)


def main() -> None:
    run_demo(MazeGenerationDemo)


if __name__ == "__main__":
    main()
