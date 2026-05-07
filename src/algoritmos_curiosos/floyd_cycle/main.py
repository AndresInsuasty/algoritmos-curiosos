from __future__ import annotations

import math

import pygame

from algoritmos_curiosos.common import (
    ACCENT,
    BACKGROUND,
    DANGER,
    MUTED,
    PANEL,
    WARNING,
    Button,
    DemoBase,
    draw_panel,
    draw_text,
    run_demo,
)
from algoritmos_curiosos.floyd_cycle.logic import advance, build_cycle_next_indices, floyd_detect


class FloydCycleDemo(DemoBase):
    title = "Floyd — la tortuga y la liebre"

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.tail_length = 4
        self.cycle_length = 6
        self.step_interval = 0.7
        self.timer = 0.0
        self.running = False
        self.steps = 0
        self.tortoise = 1
        self.hare = 2
        self.next_indices = build_cycle_next_indices(self.tail_length, self.cycle_length)
        self.result = floyd_detect(self.next_indices)
        self._build_buttons()

    def _build_buttons(self) -> None:
        y = self.height - 84
        self.buttons = [
            Button("cola −", pygame.Rect(40, y, 90, 42), "tail_down"),
            Button("cola +", pygame.Rect(138, y, 90, 42), "tail_up"),
            Button("ciclo −", pygame.Rect(254, y, 90, 42), "cycle_down"),
            Button("ciclo +", pygame.Rect(352, y, 90, 42), "cycle_up"),
            Button("Arrancar", pygame.Rect(476, y, 130, 42), "run", fill=ACCENT),
            Button("Paso", pygame.Rect(624, y, 110, 42), "step", fill=WARNING),
            Button("Reset", pygame.Rect(752, y, 110, 42), "reset", fill=DANGER),
        ]

    def reset_state(self) -> None:
        self.next_indices = build_cycle_next_indices(self.tail_length, self.cycle_length)
        self.result = floyd_detect(self.next_indices)
        self.tortoise = advance(self.next_indices, 0, 1)
        self.hare = advance(self.next_indices, 0, 2)
        self.steps = 0
        self.running = False
        self.timer = 0.0

    def on_autoplay(self) -> None:
        self.running = True

    def on_button(self, action: str) -> None:
        if action == "tail_down":
            self.tail_length = max(1, self.tail_length - 1)
            self.reset_state()
        elif action == "tail_up":
            self.tail_length = min(8, self.tail_length + 1)
            self.reset_state()
        elif action == "cycle_down":
            self.cycle_length = max(2, self.cycle_length - 1)
            self.reset_state()
        elif action == "cycle_up":
            self.cycle_length = min(12, self.cycle_length + 1)
            self.reset_state()
        elif action == "run":
            self.running = True
        elif action == "step":
            self.step_once()
        elif action == "reset":
            self.reset_state()

    def step_once(self) -> None:
        if self.steps >= self.result.steps_until_meeting:
            self.running = False
            return
        self.tortoise = advance(self.next_indices, self.tortoise, 1)
        self.hare = advance(self.next_indices, self.hare, 2)
        self.steps += 1
        if self.tortoise == self.hare:
            self.running = False

    def update(self, dt: float) -> None:
        if not self.running:
            return
        self.timer += dt
        if self.timer >= self.step_interval:
            self.timer = 0.0
            self.step_once()

    def _node_positions(self) -> list[tuple[float, float]]:
        positions: list[tuple[float, float]] = []
        circle_center = (self.width * 0.68, self.height * 0.42)
        radius = 140
        cycle_start_x = circle_center[0] - radius
        tail_start_x = 140
        tail_y = circle_center[1]

        if self.tail_length > 0:
            if self.tail_length == 1:
                positions.append((cycle_start_x - 80, tail_y))
            else:
                spacing = (cycle_start_x - 110 - tail_start_x) / (self.tail_length - 1)
                for index in range(self.tail_length):
                    positions.append((tail_start_x + spacing * index, tail_y))

        for index in range(self.cycle_length):
            angle = (2 * math.pi * index / self.cycle_length) - math.pi
            x = circle_center[0] + math.cos(angle) * radius
            y = circle_center[1] + math.sin(angle) * radius
            positions.append((x, y))

        return positions

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        panel = pygame.Rect(28, 24, self.width - 56, 156)
        draw_panel(screen, panel)
        draw_text(screen, "Detección de ciclos de Floyd", (48, 44), size=32, bold=True)
        draw_text(
            screen,
            f"Cola: {self.tail_length} nodos   Ciclo: {self.cycle_length} nodos   μ={self.result.mu}   λ={self.result.lam}",
            (48, 86),
            color=MUTED,
        )
        state = "¡Encuentro detectado!" if self.tortoise == self.hare and self.steps > 0 else "Explorando el grafo"
        draw_text(screen, f"Estado: {state}", (48, 118), color=ACCENT if self.running else WARNING)

        board = pygame.Rect(28, 200, self.width - 56, self.height - 320)
        draw_panel(screen, board)
        positions = self._node_positions()
        for index, target in enumerate(self.next_indices):
            start = positions[index]
            end = positions[target]
            pygame.draw.line(screen, PANEL, start, end, 4)
            direction = pygame.Vector2(end[0] - start[0], end[1] - start[1])
            if direction.length_squared() > 0:
                direction = direction.normalize() * 12
                arrow = (end[0] - direction.x, end[1] - direction.y)
                pygame.draw.circle(screen, PANEL, (int(arrow[0]), int(arrow[1])), 6)

        for index, position in enumerate(positions):
            color = (104, 120, 200)
            if index == self.result.meeting_index:
                color = WARNING
            if index == self.tortoise:
                color = ACCENT
            if index == self.hare:
                color = DANGER
            pygame.draw.circle(screen, color, (int(position[0]), int(position[1])), 24)
            draw_text(screen, str(index), (position[0] - 10, position[1] - 14), size=24, bold=True)

        draw_text(screen, f"Pasos: {self.steps}", (60, 620), size=28, bold=True)
        draw_text(screen, "Tortuga", (220, 620), color=ACCENT, size=26, bold=True)
        draw_text(screen, "Liebre", (340, 620), color=DANGER, size=26, bold=True)
        for button in self.buttons:
            button.draw(screen)


def main() -> None:
    run_demo(FloydCycleDemo)


if __name__ == "__main__":
    main()
