from __future__ import annotations

import random

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
    clamp,
    draw_panel,
    draw_text,
    run_demo,
)
from algoritmos_curiosos.sleep_sort.logic import SleepEvent, build_sleep_sort_schedule, generate_values


class SleepSortDemo(DemoBase):
    title = "Sleep Sort — carrera de barras"
    background = BACKGROUND

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.count = 6
        self.max_value = 12
        self.unit_seconds = 0.18
        self.rng = random.Random(7)
        self.values = generate_values(self.count, self.max_value, seed=7)
        self.pending_events: list[SleepEvent] = []
        self.sorted_values: list[SleepEvent] = []
        self.running = False
        self.elapsed = 0.0
        self._build_buttons()

    def _build_buttons(self) -> None:
        y = self.height - 84
        self.buttons = [
            Button("−", pygame.Rect(40, y, 50, 42), "count_down"),
            Button("+", pygame.Rect(96, y, 50, 42), "count_up"),
            Button("max −", pygame.Rect(186, y, 90, 42), "max_down"),
            Button("max +", pygame.Rect(284, y, 90, 42), "max_up"),
            Button("Mezclar", pygame.Rect(424, y, 130, 42), "shuffle", fill=WARNING),
            Button("Correr", pygame.Rect(572, y, 130, 42), "run", fill=ACCENT),
            Button("Reset", pygame.Rect(720, y, 130, 42), "reset", fill=DANGER),
        ]

    def on_autoplay(self) -> None:
        self.start()

    def start(self) -> None:
        self.elapsed = 0.0
        self.sorted_values.clear()
        self.pending_events = build_sleep_sort_schedule(self.values, self.unit_seconds)
        self.running = True

    def reset(self) -> None:
        self.running = False
        self.elapsed = 0.0
        self.sorted_values.clear()
        self.pending_events.clear()

    def shuffle(self) -> None:
        self.values = [self.rng.randint(1, self.max_value) for _ in range(self.count)]
        self.reset()

    def on_button(self, action: str) -> None:
        if action == "count_down":
            self.count = max(3, self.count - 1)
            self.values = self.values[: self.count]
            self.reset()
        elif action == "count_up":
            self.count = min(10, self.count + 1)
            self.values = generate_values(self.count, self.max_value, seed=self.rng.randint(0, 9999))
            self.reset()
        elif action == "max_down":
            self.max_value = max(4, self.max_value - 1)
            self.values = [min(value, self.max_value) for value in self.values]
            self.reset()
        elif action == "max_up":
            self.max_value = min(20, self.max_value + 1)
        elif action == "shuffle":
            self.shuffle()
        elif action == "run":
            self.start()
        elif action == "reset":
            self.reset()

    def update(self, dt: float) -> None:
        if not self.running:
            return

        self.elapsed += dt
        while self.pending_events and self.pending_events[0].release_time <= self.elapsed:
            self.sorted_values.append(self.pending_events.pop(0))

        if not self.pending_events:
            self.running = False

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.background)
        panel = pygame.Rect(28, 24, self.width - 56, 156)
        draw_panel(screen, panel)
        draw_text(screen, "Sleep Sort: cada barra 'despierta' según su valor.", (48, 44), size=32, bold=True)
        draw_text(
            screen,
            f"Cantidad: {self.count}   Máximo: {self.max_value}   Retardo base: {self.unit_seconds:.2f}s",
            (48, 86),
            color=MUTED,
        )
        state = "Corriendo..." if self.running else "Listo para iniciar"
        draw_text(screen, f"Estado: {state}", (48, 118), color=ACCENT if self.running else WARNING)

        queue_area = pygame.Rect(40, 210, self.width - 80, 200)
        sorted_area = pygame.Rect(40, 440, self.width - 80, 180)
        draw_panel(screen, queue_area)
        draw_panel(screen, sorted_area)
        draw_text(screen, "Cola inicial", (56, 220), size=28, bold=True)
        draw_text(screen, "Salida ordenada", (56, 450), size=28, bold=True)

        bar_width = max(48, (queue_area.width - 80) // max(1, len(self.values)))
        max_bar_height = 110
        for index, value in enumerate(self.values):
            x = queue_area.x + 26 + index * bar_width
            height = int(max_bar_height * (value / max(1, self.max_value)))
            rect = pygame.Rect(x, queue_area.bottom - 28 - height, bar_width - 12, height)
            color = (92, 160 + (value * 4) % 80, 255 - (value * 5) % 90)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            draw_text(screen, str(value), (rect.x + 12, rect.y - 28), size=24)

        for index, event in enumerate(self.sorted_values):
            x = sorted_area.x + 26 + index * bar_width
            height = int(max_bar_height * (event.value / max(1, self.max_value)))
            rect = pygame.Rect(x, sorted_area.bottom - 24 - height, bar_width - 12, height)
            pygame.draw.rect(screen, ACCENT, rect, border_radius=8)
            draw_text(screen, str(event.value), (rect.x + 12, rect.y - 28), size=24)

        if self.running and self.pending_events:
            current = self.pending_events[0]
            progress = clamp(self.elapsed / max(current.release_time, 0.001), 0.0, 1.0)
            draw_text(
                screen,
                f"Próxima barra: {current.value} en {max(0.0, current.release_time - self.elapsed):.2f}s",
                (56, 640),
                color=WARNING,
                size=26,
            )
            pygame.draw.rect(screen, PANEL, (56, 676, 360, 16), border_radius=8)
            pygame.draw.rect(screen, ACCENT, (56, 676, int(360 * progress), 16), border_radius=8)

        for button in self.buttons:
            button.draw(screen)


def main() -> None:
    run_demo(SleepSortDemo)


if __name__ == "__main__":
    main()
