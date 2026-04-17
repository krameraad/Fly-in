from enum import Enum, auto
from dataclasses import dataclass, field

import pygame
from pygame import Vector2

import assets


class ZoneType(Enum):
    NORMAL = auto()         # Normal path.
    BLOCKED = auto()        # Inaccessible.
    RESTRICTED = auto()     # 2-turn movement.
    PRIORITY = auto()       # 1-turn, preferred if possible.
    START = auto()          # Start.
    END = auto()            # End.


@dataclass
class Zone:
    """Node in a network of zones that can be traversed by drones."""
    name: str
    x: int
    y: int
    zonetype: ZoneType = ZoneType.NORMAL
    color: str = 'white'
    max_drones: int = 1
    links: list[tuple['Zone', int]] = field(default_factory=list)
    """List of connections as
    a tuple of connected `Zone` and `max_link_capacity`."""

    def __post_init__(self) -> None:
        self.drone_load = 0
        self.pos = Vector2(self.x * 128, self.y * 128)

        self.img = assets.get_colored(
            f'zone_{self.zonetype.name.lower}', self.color)
        self.rect = self.img.get_rect(center=self.pos)
        self.label = assets.IMG['label']
        self.label_rect = self.label.get_rect(
            left=self.pos.x - 64,
            top=self.pos.y - 32,
        )

        self.labeltext = pygame.font.Font.render(
            assets.FONT,
            f'{self.max_drones:>2}',
            True,
            (255, 255, 255)
        )
        self.labeltext_rect = self.labeltext.get_rect(
            left=self.pos.x + 16,
            top=self.pos.y + 19,
        )

    def __str__(self) -> str:
        result = \
            f'{self.name:<24} {self.x:>4} {self.y:>4} ' \
            f'{self.zonetype.name.capitalize():<12} ' \
            f'{self.color.capitalize():<12} {self.max_drones:>2}'
        linknames = [x[0].name for x in self.links]
        return f'{result}\n\033[2m└─> {", ".join(linknames)}\033[0m'

    def draw(self, screen: pygame.Surface, offset: tuple) -> None:
        screen.blit(
            self.img,
            self.rect.move(*offset)
        )
        if self.max_drones != 1:
            screen.blit(
                self.label,
                self.label_rect.move(*offset),
            )
            screen.blit(
                self.labeltext,
                self.labeltext_rect.move(*offset),
                (0, 0, 128, 21)
            )
