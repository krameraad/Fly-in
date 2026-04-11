from dataclasses import dataclass

import pygame

import assets
from zone import Zone, ZoneType


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
        self.zone.max_drones -= 1

    def move(self, destination: Zone) -> None:
        "Move to any zone. Does not check if the move is legal."
        self.zone.max_drones += 1
        destination.max_drones -= 1
        self.zone = destination

    def find_path(self, graph: list[Zone], goal: Zone) -> list[Zone]:
        "Implementation of Dijkstra's algorithm."
        g = {
            x.name: {
                'zone': x,
                'cost': float('inf'),
                'prev': None
            }
            for x in graph
            if x.zonetype != ZoneType.BLOCKED
            # and x.max_drones > 0
        }

        visited = set()
        queue = [self.zone]
        g[self.zone.name]['cost'] = 0

        while queue:
            for link in queue[0].links:
                if link[0].zonetype == ZoneType.BLOCKED:
                    continue
                if link[0].name not in visited:
                    queue.append(link[0])

                current = g[queue[0].name]
                neighbor = g[link[0].name]
                distance = int(
                    neighbor['zone'].zonetype == ZoneType.RESTRICTED
                ) + 1
                if current['cost'] + distance < neighbor['cost']:
                    neighbor['cost'] = current['cost'] + distance
                    neighbor['prev'] = current['zone']

            visited.add(queue[0].name)
            queue.pop(0)

        # Collapse path
        path = []
        current = g[goal.name]
        while current['prev']:
            path.append(current['zone'])
            current = g[current['prev'].name]
        path.reverse()
        return path

    def draw(self, screen: pygame.Surface, offset: tuple) -> None:
        screen.blit(
            self.img,
            self.rect.move(*offset)
        )
