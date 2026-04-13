from dataclasses import dataclass

import pygame
from pygame import Vector2

import assets
from zone import Zone, ZoneType


@dataclass
class Drone:
    """Drone that moves between nodes."""
    name: str
    zone: Zone

    def __post_init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.speed = Vector2(0, 0)
        self.img = assets.IMG['drone']
        self.rect = self.img.get_rect(center=(self.pos.x, self.pos.y))
        self.lagged = False
        self.path = []

        self.zone.drone_load += 1

    def move(self) -> None:
        """Move to the next zone. Does not check if the move is legal,
        only if the destination is `None`."""
        if not self.path:
            return
        destination = self.path[0]
        if destination.drone_load >= destination.max_drones \
                and destination.zonetype != ZoneType.END:
            return
        if self.lagged:
            self.lagged = False
            return
        if destination.zonetype == ZoneType.RESTRICTED:
            self.lagged = True
        print(f'{self.name}-{destination.name}', end=' ')
        self.zone.drone_load -= 1
        destination.drone_load += 1
        self.zone = self.path.pop(0)

    def dijkstras(
            self,
            graph: list[Zone],
            goal: Zone,
            traffic: dict[str, int]
            ) -> list[Zone]:
        """Implementation of Dijkstra's algorithm.

        Args:
            graph: List of all zones that make up the network.
            goal: Zone to find a path to.
            traffic: Map of congestion for each node.

        Returns:
            List of zones that make up the path,
            or an empty list if no path could be found."""
        # Make a table with the necessary information for each zone.
        g = {
            x.name: {
                'zone': x,
                'cost': float('inf'),
                'prev': None
            }
            for x in graph
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
                distance = 100 + (100 * traffic[link[0].name])
                if neighbor['zone'].zonetype == ZoneType.RESTRICTED:
                    distance *= 2
                if neighbor['zone'].zonetype == ZoneType.PRIORITY:
                    distance //= 2
                if current['cost'] + distance < neighbor['cost']:
                    neighbor['cost'] = current['cost'] + distance
                    neighbor['prev'] = current['zone']

            visited.add(queue[0].name)
            queue.pop(0)

        # Collapse the path.
        path: list[Zone] = []
        current = g[goal.name]
        while current['prev']:
            path.append(current['zone'])
            current = g[current['prev'].name]
        path.reverse()

        # Print the path for debugging purposes.
        # print('\nPath:')
        # for i, x in enumerate(path):
        #     print(i, ':', x.name)

        self.path = path
        return path

    def update(self) -> None:
        self.speed *= 0.75
        wishdir = self.zone.pos - self.pos
        if wishdir.length() > 16:
            self.speed += (self.zone.pos - self.pos).normalize() * 3
        else:
            self.speed *= 0.5
        self.pos += self.speed

    def draw(self, screen: pygame.Surface, offset: tuple) -> None:
        screen.blit(
            self.img,
            self.rect.move(
                (self.pos.x + offset[0], self.pos.y + offset[1])
            )
        )
