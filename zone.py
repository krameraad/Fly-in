from enum import Enum, auto
from dataclasses import dataclass


class ZoneType(Enum):
    NORMAL = auto()
    BLOCKED = auto()
    RESTRICT = auto()
    PRIORITY = auto()
    START = auto()
    END = auto()


@dataclass
class Zone:
    """Node in a network of zones that can be traversed by drones."""
    name: str
    x: int
    y: int
    zonetype = ZoneType.NORMAL
    color = 'none'
    max_drones = 1
    connections: list[tuple['Zone', int]] = []
    """List of connections as
    a tuple of connected `Zone` and `max_link_capacity`."""
