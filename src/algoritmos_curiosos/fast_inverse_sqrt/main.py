from __future__ import annotations

import math

import pygame

from algoritmos_curiosos.common import (
    ACCENT,
    BACKGROUND,
    DANGER,
    MUTED,
    WARNING,
    Button,
    DemoBase,
    clamp,
    draw_panel,
    draw_text,
    run_demo,
)
from algoritmos_curiosos.fast_inverse_sqrt.logic import exact_inverse_sqrt, fast_inverse_sqrt


class FastInverseSqrtDemo(DemoBase):
    title = "Fast Inverse Square Root — persecución espacial"

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.iterations = 1
        self.speed = 180.0
        self.target = pygame.Vector2(width * 0.76, height * 0.32)
        self.target_velocity = pygame.Vector2(-180, 140)
        self.exact_ship = pygame.Vector2(width * 0.24, height * 0.72)
        self.fast_ship = pygame.Vector2(width * 0.20, height * 0.76)
        self.exact_trail: list[tuple[float, float]] = []
        self.fast_trail: list[tuple[float, float]] = []
        self._build_buttons()

    def _build_buttons(self) -> None:
        y = self.height - 84
        self.buttons = [
            Button("iter −", pygame.Rect(40, y, 90, 42), "iter_down"),
            Button("iter +", pygame.Rect(138, y, 90, 42), "iter_up"),
            Button("vel −", pygame.Rect(254, y, 90, 42), "speed_down"),
            Button("vel +", pygame.Rect(352, y, 90, 42), "speed_up"),
            Button("Reset", pygame.Rect(476, y, 120, 42), "reset", fill=DANGER),
        ]

    def on_button(self, action: str) -> None:
        if action == "iter_down":
            self.iterations = max(0, self.iterations - 1)
        elif action == "iter_up":
            self.iterations = min(3, self.iterations + 1)
        elif action == "speed_down":
            self.speed = max(60.0, self.speed - 30.0)
        elif action == "speed_up":
            self.speed = min(360.0, self.speed + 30.0)
        elif action == "reset":
            self.exact_ship = pygame.Vector2(self.width * 0.24, self.height * 0.72)
            self.fast_ship = pygame.Vector2(self.width * 0.20, self.height * 0.76)
            self.exact_trail.clear()
            self.fast_trail.clear()

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.target = pygame.Vector2(event.pos)

    def _move_ship(self, ship: pygame.Vector2, inv_sqrt: float, dt: float) -> None:
        delta = self.target - ship
        if delta.length_squared() < 1e-5:
            return
        ship += delta * inv_sqrt * self.speed * dt

    def update(self, dt: float) -> None:
        self.target += self.target_velocity * dt
        if self.target.x < 200 or self.target.x > self.width - 120:
            self.target_velocity.x *= -1
        if self.target.y < 180 or self.target.y > self.height - 180:
            self.target_velocity.y *= -1

        exact_delta = self.target - self.exact_ship
        fast_delta = self.target - self.fast_ship
        if exact_delta.length_squared() > 0.001:
            exact_inv = exact_inverse_sqrt(exact_delta.length_squared())
            self._move_ship(self.exact_ship, exact_inv, dt)
        if fast_delta.length_squared() > 0.001:
            fast_inv = fast_inverse_sqrt(fast_delta.length_squared(), self.iterations)
            self._move_ship(self.fast_ship, fast_inv, dt)

        self.exact_trail.append((self.exact_ship.x, self.exact_ship.y))
        self.fast_trail.append((self.fast_ship.x, self.fast_ship.y))
        self.exact_trail = self.exact_trail[-120:]
        self.fast_trail = self.fast_trail[-120:]

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        panel = pygame.Rect(28, 24, self.width - 56, 156)
        draw_panel(screen, panel)
        delta = self.target - self.fast_ship
        distance_sq = max(delta.length_squared(), 0.001)
        approx = fast_inverse_sqrt(distance_sq, self.iterations)
        exact = exact_inverse_sqrt(distance_sq)
        error = abs(approx - exact) / exact * 100
        draw_text(screen, "Fast Inverse Square Root", (48, 42), size=32, bold=True)
        draw_text(
            screen,
            f"Iteraciones Newton: {self.iterations}   Velocidad: {self.speed:.0f} px/s   Error actual: {error:.3f}%",
            (48, 84),
            color=MUTED,
        )
        draw_text(
            screen,
            f"Pulsa en la escena para mover el objetivo. El dron cian usa sqrt exacta, el magenta usa el truco de Quake III.",
            (48, 118),
            color=WARNING,
            size=22,
        )

        arena = pygame.Rect(28, 200, self.width - 56, self.height - 320)
        draw_panel(screen, arena)
        for index, point in enumerate(self.exact_trail):
            alpha = 80 + int(175 * (index / max(1, len(self.exact_trail))))
            pygame.draw.circle(screen, (80, 240, 240, alpha), (int(point[0]), int(point[1])), 2)
        for index, point in enumerate(self.fast_trail):
            alpha = 80 + int(175 * (index / max(1, len(self.fast_trail))))
            pygame.draw.circle(screen, (255, 90, 220, alpha), (int(point[0]), int(point[1])), 2)

        pygame.draw.circle(screen, WARNING, (int(self.target.x), int(self.target.y)), 18)
        pygame.draw.circle(screen, ACCENT, (int(self.exact_ship.x), int(self.exact_ship.y)), 14)
        pygame.draw.circle(screen, (255, 90, 220), (int(self.fast_ship.x), int(self.fast_ship.y)), 14)
        pygame.draw.line(screen, ACCENT, self.exact_ship, self.target, 2)
        pygame.draw.line(screen, (255, 90, 220), self.fast_ship, self.target, 2)

        comparison_center = pygame.Vector2(160, 560)
        mouse_delta = self.target - comparison_center
        if mouse_delta.length_squared() > 0.001:
            exact_dir = mouse_delta * exact_inverse_sqrt(mouse_delta.length_squared()) * 80
            fast_dir = mouse_delta * fast_inverse_sqrt(mouse_delta.length_squared(), self.iterations) * 80
            pygame.draw.circle(screen, (60, 72, 104), (int(comparison_center.x), int(comparison_center.y)), 44, 2)
            pygame.draw.line(screen, ACCENT, comparison_center, comparison_center + exact_dir, 5)
            pygame.draw.line(screen, (255, 90, 220), comparison_center, comparison_center + fast_dir, 3)
            draw_text(screen, "Normalización del vector", (80, 610), size=22, color=MUTED)

        for button in self.buttons:
            button.draw(screen)


def main() -> None:
    run_demo(FastInverseSqrtDemo)


if __name__ == "__main__":
    main()
