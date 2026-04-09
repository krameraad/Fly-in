from dataclasses import dataclass

import pygame

import assets
from zone import Zone


@dataclass
class Drone:
    """Drone that moves between nodes."""
    name: str
    zone: Zone
    x: int = 0
    y: int = 0

    def __post_init__(self) -> None:
        self.img = assets.IMG['drone']
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface, offset: tuple) -> None:
        screen.blit(self.img, self.rect.move(*offset))
