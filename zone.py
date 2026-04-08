from enum import Enum, auto
from dataclasses import dataclass, field


class ZoneType(Enum):
    NORMAL = auto()     # Normal path.
    BLOCKED = auto()    # Inaccessible.
    RESTRICT = auto()   # 2-turn movement.
    PRIORITY = auto()   # 1-turn, preferred if possible.
    START = auto()      # Start.
    END = auto()        # End.


@dataclass
class Zone:
    """Node in a network of zones that can be traversed by drones."""
    name: str
    x: int
    y: int
    zonetype = ZoneType.NORMAL
    color = 'none'
    max_drones = 1
    connections: list[tuple['Zone', int]] = field(default_factory=list)
    """List of connections as
    a tuple of connected `Zone` and `max_link_capacity`."""
