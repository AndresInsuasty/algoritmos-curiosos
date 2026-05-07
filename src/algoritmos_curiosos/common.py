from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import pygame

BACKGROUND = (18, 18, 32)
PANEL = (33, 35, 58)
PANEL_BORDER = (96, 100, 150)
TEXT = (244, 245, 255)
MUTED = (170, 176, 210)
ACCENT = (92, 220, 189)
WARNING = (255, 187, 92)
DANGER = (255, 110, 110)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def parse_demo_args(title: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--frames", type=int, default=0)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--autoplay", action="store_true")
    parser.add_argument("--screenshot", type=str)
    return parser.parse_args()


def initialize_pygame(headless: bool) -> None:
    if headless and "SDL_VIDEODRIVER" not in os.environ:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    if headless and "SDL_AUDIODRIVER" not in os.environ:
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.init()
    pygame.font.init()


def font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("arial", size, bold=bold)


def draw_text(
    screen: pygame.Surface,
    text: str,
    position: tuple[float, float],
    *,
    size: int = 24,
    color: tuple[int, int, int] = TEXT,
    bold: bool = False,
) -> None:
    surface = font(size, bold=bold).render(text, True, color)
    screen.blit(surface, position)


def draw_panel(screen: pygame.Surface, rect: pygame.Rect) -> None:
    pygame.draw.rect(screen, PANEL, rect, border_radius=16)
    pygame.draw.rect(screen, PANEL_BORDER, rect, 2, border_radius=16)


@dataclass
class Button:
    label: str
    rect: pygame.Rect
    action: str
    fill: tuple[int, int, int] = PANEL
    text_color: tuple[int, int, int] = TEXT

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.fill, self.rect, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, self.rect, 2, border_radius=12)
        label_surface = font(22, bold=True).render(self.label, True, self.text_color)
        label_rect = label_surface.get_rect(center=self.rect.center)
        screen.blit(label_surface, label_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class DemoBase:
    title = "Demo"
    background = BACKGROUND

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.buttons: list[Button] = []

    def on_autoplay(self) -> None:
        """Start the animation automatically when requested."""

    def handle_event(self, event: pygame.event.Event) -> None:
        for button in self.buttons:
            if button.is_clicked(event):
                self.on_button(button.action)
                return

    def on_button(self, action: str) -> None:
        """React to button actions."""

    def update(self, dt: float) -> None:
        """Advance the simulation."""

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.background)
        for button in self.buttons:
            button.draw(screen)


def run_demo(demo_type: type[DemoBase]) -> None:
    args = parse_demo_args(demo_type.title)
    initialize_pygame(args.headless)
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption(demo_type.title)
    clock = pygame.time.Clock()
    demo = demo_type(args.width, args.height)
    if args.autoplay:
        demo.on_autoplay()

    frame_limit = args.frames if args.frames > 0 else None
    frames = 0
    running = True

    while running:
        dt = clock.tick(args.fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                demo.handle_event(event)

        demo.update(dt)
        demo.draw(screen)
        pygame.display.flip()

        frames += 1
        if frame_limit is not None and frames >= frame_limit:
            running = False

    if args.screenshot:
        screenshot_dir = os.path.dirname(args.screenshot)
        if screenshot_dir:
            os.makedirs(screenshot_dir, exist_ok=True)
        pygame.image.save(screen, args.screenshot)

    pygame.quit()
