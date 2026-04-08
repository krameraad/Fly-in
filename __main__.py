import sys
from pathlib import Path

import pygame

# from zone import Zone
from parser import parse
from builder import build


data = parse(Path(sys.argv[1]))
zones = build(data)
start, end = data['start_hub']['name'], data['end_hub']['name']


print(f"\033[1m{'Zone':<24} {'x':>4} {'y':>4} {'Type':<12} "
      f"{'Color':<6} {'Capacity'}\033[0m\n",
      '\033[2m', "-" * 63, '\033[0m', sep='')
for k, v in zones.items():
    print(v)


pygame.init()

w, h = 800, 600
unit = 64  # Pixel size of one unit of distance between nodes.
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Fly-in')
clock = pygame.time.Clock()

img_zone = pygame.image.load("assets/zone_normal.png").convert_alpha()
rect_zone = img_zone.get_rect(center=(32, 32))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(img_zone, rect_zone)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
