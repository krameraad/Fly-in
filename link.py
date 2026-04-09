from dataclasses import dataclass

import pygame


@dataclass
class Link:
    """Node in a network of zones that can be traversed by drones."""
    start: tuple[int, int]
    end: tuple[int, int]
    max_link_capacity: int = 1

    def __post_init__(self) -> None:
        self.thickness = 4 * self.max_link_capacity

    def draw(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        pygame.draw.line(
            screen,
            (0, 0, 0),
            tuple(x + y for x, y in zip(self.start, offset)),
            tuple(x + y for x, y in zip(self.end, offset)),
            self.thickness + 4,
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            tuple(x + y for x, y in zip(self.start, offset)),
            tuple(x + y for x, y in zip(self.end, offset)),
            self.thickness,
        )
