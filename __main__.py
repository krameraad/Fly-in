import sys
from pathlib import Path
from dataclasses import dataclass

import pygame

import assets
# from zone import Zone
from link import Link
from parser import parse
from builder import build


@dataclass
class Context:
    cam_x: int = 0
    cam_y: int = 0
    camspeed_x: float = 0.0
    camspeed_y: float = 0.0

    def update(self) -> None:
        self.camspeed_x *= 0.9
        self.camspeed_y *= 0.9
        self.cam_x = round(self.cam_x + self.camspeed_x)
        self.cam_y = round(self.cam_y + self.camspeed_y)

    def get_offset(self) -> tuple[int, int]:
        return (self.cam_x, self.cam_y)


pygame.init()

w, h = 1600, 1200
unit = 128  # Pixel size of one unit of distance between nodes.
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Fly-in')
clock = pygame.time.Clock()
pygame.key.set_repeat(1)

assets.load_assets(Path('assets'))
# bg_rect = assets.IMG['bg'].get_rect(center=(800, 600))

ctx = Context(w // 2, h // 2)
data = parse(Path(sys.argv[1]), unit)
zones = build(data)
start, end = data['start_hub']['name'], data['end_hub']['name']
links = [Link(zones[x[0]].pos(), zones[x[1]].pos(), x[2])
         for x in data['links']]


print(f"\033[1m{'Zone':<24} {'x':>4} {'y':>4} {'Type':<12} "
      f"{'Color':<6} {'Capacity'}\033[0m\n",
      '\033[2m', "-" * 63, '\033[0m', sep='')
for k, v in zones.items():
    print(v)


running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_LEFT]:
            ctx.camspeed_x += 0.2
        if keys[pygame.K_RIGHT]:
            ctx.camspeed_x -= 0.2
        if keys[pygame.K_UP]:
            ctx.camspeed_y += 0.2
        if keys[pygame.K_DOWN]:
            ctx.camspeed_y -= 0.2

    ctx.update()
    screen.fill((100, 100, 100))
    # screen.blit(assets.IMG['bg'], bg_rect)
    for x in links:
        x.draw(screen, ctx.get_offset())
    for k, v in zones.items():
        v.draw(screen, ctx.get_offset())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
