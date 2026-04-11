from dataclasses import dataclass

import pygame

import assets
from zone import Zone


@dataclass
class Drone:
    """Drone that moves between nodes."""
    name: str
    zone: Zone
    goal: Zone
    x: int = 0
    y: int = 0

    def __post_init__(self) -> None:
        self.img = assets.IMG['drone']
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.zone.max_drones -= 1

    def move(self, destination: Zone) -> None:
        """Move a drone towards an adjacent zone.
        Does not check if the move is legal."""
        self.zone.max_drones += 1
        destination.max_drones -= 1
        self.zone = destination

    def find_path(self) -> None:
        # visited = set()
        # queue = [self.zone]
        ...

    def draw(self, screen: pygame.Surface, offset: tuple) -> None:
        screen.blit(
            self.img,
            self.rect.move(*offset)
        )
