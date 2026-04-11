import sys
from pathlib import Path
from dataclasses import dataclass

import pygame
from pygame import Vector2

import assets
from zone import Zone
from drone import Drone
from link import Link
from parser import parse
from builder import build


def execute_turn(
        graph: list[Zone],
        goal: Zone,
        drones: list[Drone]
        ) -> None:
    for drone in drones:
        if drone.zone is goal:
            continue
        path = drone.dijkstras(graph, goal)
        if path:
            drone.move(path[0])
    print()


pygame.init()

w, h = 1600, 1200
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Fly-in')
clock = pygame.time.Clock()

assets.load_assets(Path('assets'))
# bg_rect = assets.IMG['bg'].get_rect(center=(800, 600))

cam = Vector2(w // 2, h // 2)
data = parse(Path(sys.argv[1]))
zones = build(data)
start, end = data['start_hub']['name'], data['end_hub']['name']
links = [Link(zones[x[0]].pos, zones[x[1]].pos, x[2])
         for x in data['links']]
drones = [Drone(f'D{i + 1}', zones[start])
          for i in range(data['nb_drones'])]


print(f'\033[1mNumber of drones: {data['nb_drones']}\033[0m')
print(f"\033[1m{'Zone':<24} {'x':>4} {'y':>4} {'Type':<12} "
      f"{'Color':<6} {'Capacity'}\033[0m\n",
      '\033[2m', "-" * 63, '\033[0m', sep='')
for x in zones.values():
    print(x)


ui_1 = pygame.font.Font.render(
    assets.FONT_BIG,
    'Mouse 1: Advance simulation.',
    True,
    (255, 255, 255),
    (0, 0, 0)
)
ui_1_rect = ui_1.get_rect(left=16, top=16)
ui_2 = pygame.font.Font.render(
    assets.FONT_BIG,
    'Mouse 2: Pan the screen.',
    True,
    (255, 255, 255),
    (0, 0, 0)
)
ui_2_rect = ui_2.get_rect(left=16, top=64)


running = True
while running:
    for event in pygame.event.get():
        mouse_movement = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[2]:
            cam += Vector2(mouse_movement)

        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                execute_turn(list(zones.values()), zones[end], drones)

    screen.fill((100, 100, 100))
    # screen.blit(assets.IMG['bg'], bg_rect)
    for x in links:
        x.draw(screen, cam)
    for x in zones.values():
        x.draw(screen, cam)
    for x in drones:
        x.update()
        x.draw(screen, cam)

    screen.blit(ui_1, ui_1_rect)
    screen.blit(ui_2, ui_2_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
