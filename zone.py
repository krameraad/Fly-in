from enum import Enum, auto
from dataclasses import dataclass, field


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

    def __str__(self) -> str:
        result = \
            f'{self.name:<24} {self.x:>4} {self.y:>4} ' \
            f'{self.zonetype.name.capitalize():<12} ' \
            f'{self.color.capitalize():<12} {self.max_drones:>2}'
        linknames = [x[0].name for x in self.links]
        return f'{result}\n\033[2m└─> {", ".join(linknames)}\033[0m'
