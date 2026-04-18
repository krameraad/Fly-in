from dataclasses import dataclass

import pygame
from pygame import Vector2


@dataclass
class Link:
    """Link to be drawn in the graphical display. No functionality."""
    start: tuple[int, int]
    end: tuple[int, int]
    max_link_capacity: int = 1

    def __post_init__(self) -> None:
        self.thickness = 6 * self.max_link_capacity

    def draw(self, screen: pygame.Surface, offset: Vector2) -> None:
        "Draw this object to `screen` with camera `offset`."
        pygame.draw.line(
            screen,
            (0, 0, 0),
            self.start + offset,
            self.end + offset,
            self.thickness + 6,
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            self.start + offset,
            self.end + offset,
            self.thickness,
        )
