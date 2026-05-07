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
from algoritmos_curiosos.bogosort.logic import bogosort_step, is_sorted, quantum_bogosort


class BogosortDemo(DemoBase):
    title = "Bogosort y Quantum Bogosort"

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.count = 5
        self.algorithm = "Bogosort"
        self.values = [5, 1, 4, 2, 3]
        self.rng = random.Random(11)
        self.shuffle_interval = 0.25
        self.elapsed = 0.0
        self.running = False
        self.flash = 0.0
        self.attempts = 0
        self._build_buttons()

    def _build_buttons(self) -> None:
        y = self.height - 84
        self.buttons = [
            Button("n −", pygame.Rect(40, y, 70, 42), "count_down"),
            Button("n +", pygame.Rect(118, y, 70, 42), "count_up"),
            Button("Modo", pygame.Rect(214, y, 110, 42), "toggle_mode"),
            Button("Mezclar", pygame.Rect(350, y, 130, 42), "shuffle", fill=WARNING),
            Button("Lanzar", pygame.Rect(498, y, 130, 42), "run", fill=ACCENT),
            Button("Reset", pygame.Rect(646, y, 130, 42), "reset", fill=DANGER),
        ]

    def reset_values(self) -> None:
        self.values = list(range(1, self.count + 1))
        self.rng.shuffle(self.values)
        self.attempts = 0
        self.running = False
        self.flash = 0.0

    def on_autoplay(self) -> None:
        self.running = True

    def on_button(self, action: str) -> None:
        if action == "count_down":
            self.count = max(3, self.count - 1)
            self.reset_values()
        elif action == "count_up":
            self.count = min(7, self.count + 1)
            self.reset_values()
        elif action == "toggle_mode":
            self.algorithm = "Quantum Bogosort" if self.algorithm == "Bogosort" else "Bogosort"
            self.reset_values()
        elif action == "shuffle":
            self.reset_values()
        elif action == "run":
            self.running = True
        elif action == "reset":
            self.reset_values()

    def update(self, dt: float) -> None:
        if self.flash > 0:
            self.flash = max(0.0, self.flash - dt)

        if not self.running:
            return

        self.elapsed += dt
        if self.elapsed < self.shuffle_interval:
            return
        self.elapsed = 0.0

        if self.algorithm == "Bogosort":
            if is_sorted(self.values):
                self.running = False
                return
            self.values = bogosort_step(self.values, self.rng)
            self.attempts += 1
        else:
            self.flash = 0.9
            self.values = quantum_bogosort(self.values)
            self.attempts = 1
            self.running = False

    def draw(self, screen: pygame.Surface) -> None:
        intensity = int(110 * self.flash)
        screen.fill((BACKGROUND[0] + intensity, BACKGROUND[1], BACKGROUND[2] + intensity))
        panel = pygame.Rect(28, 24, self.width - 56, 156)
        draw_panel(screen, panel)
        draw_text(screen, "Bogosort vs Quantum Bogosort", (48, 42), size=32, bold=True)
        draw_text(
            screen,
            f"Modo: {self.algorithm}   Elementos: {self.count}   Intentos: {self.attempts}",
            (48, 84),
            color=MUTED,
        )
        description = (
            "Bogosort baraja hasta acertar. Quantum Bogosort 'colapsa' directamente al universo ordenado."
        )
        draw_text(screen, description, (48, 118), color=WARNING, size=22)

        board = pygame.Rect(28, 210, self.width - 56, self.height - 320)
        draw_panel(screen, board)
        bar_width = max(60, (board.width - 100) // max(1, len(self.values)))
        max_height = board.height - 100
        for index, value in enumerate(self.values):
            x = board.x + 44 + index * bar_width
            height = int(max_height * (value / max(self.values)))
            rect = pygame.Rect(x, board.bottom - 40 - height, bar_width - 18, height)
            color = ACCENT if is_sorted(self.values) else (140 + value * 10, 90, 210 - value * 10)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            draw_text(screen, str(value), (rect.x + 14, rect.y - 28), size=24)

        if self.algorithm == "Quantum Bogosort" and self.flash > 0:
            draw_text(screen, "⚛️ MEDICIÓN CUÁNTICA EXITOSA ⚛️", (360, 620), color=WARNING, size=28, bold=True)
        elif self.running:
            draw_text(screen, "Barajando universos posibles...", (420, 620), color=WARNING, size=28, bold=True)

        for button in self.buttons:
            button.draw(screen)


def main() -> None:
    run_demo(BogosortDemo)


if __name__ == "__main__":
    main()
