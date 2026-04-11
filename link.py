from dataclasses import dataclass

import pygame


@dataclass
class Link:
    """Link to be drawn in the graphical display. No functionality."""
    start: tuple[int, int]
    end: tuple[int, int]
    max_link_capacity: int = 1

    def __post_init__(self) -> None:
        self.thickness = 6 * self.max_link_capacity

    def draw(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.start[0] + offset[0], self.start[1] + offset[1]),
            (self.end[0] + offset[0], self.end[1] + offset[1]),
            self.thickness + 6,
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.start[0] + offset[0], self.start[1] + offset[1]),
            (self.end[0] + offset[0], self.end[1] + offset[1]),
            self.thickness,
        )
