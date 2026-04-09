import sys
from pathlib import Path
from dataclasses import dataclass

import pygame

import assets
# from zone import Zone
from parser import parse
from builder import build


@dataclass
class Context:
    cam_x: int = 0
    cam_y: int = 0


pygame.init()

w, h = 1600, 1200
unit = 128  # Pixel size of one unit of distance between nodes.
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Fly-in')
clock = pygame.time.Clock()
pygame.key.set_repeat(1)

assets.load_assets(Path('assets'))


ctx = Context(w // 2, h // 2)
data = parse(Path(sys.argv[1]), unit)
zones = build(data)
start, end = data['start_hub']['name'], data['end_hub']['name']


print(f"\033[1m{'Zone':<24} {'x':>4} {'y':>4} {'Type':<12} "
      f"{'Color':<6} {'Capacity'}\033[0m\n",
      '\033[2m', "-" * 63, '\033[0m', sep='')
for k, v in zones.items():
    print(v)


running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_LEFT]:
            ctx.cam_x -= 1
        if keys[pygame.K_RIGHT]:
            ctx.cam_x += 1
        if keys[pygame.K_UP]:
            ctx.cam_y -= 1
        if keys[pygame.K_DOWN]:
            ctx.cam_y += 1

    screen.fill((30, 30, 30))
    for k, v in zones.items():
        v.draw(screen, (ctx.cam_x, ctx.cam_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
