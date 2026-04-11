import sys
from pathlib import Path

import pygame
from pygame import Vector2

import assets
from zone import Zone
from drone import Drone
from link import Link
from parser import parse
from builder import build


turncount = 0


def execute_turn(
        zones: dict[str, Zone],
        goal: Zone,
        drones: list[Drone]
        ) -> None:
    "Allow all drones to make a move towards the goal."
    global turncount
    if all([drone.zone is goal for drone in drones]):
        return
    turncount += 1
    loadmap = {k: v.drone_load for k, v in zones.items()}
    for drone in drones:
        if drone.zone is goal:
            continue
        path = drone.dijkstras(list(zones.values()), goal, loadmap)
        if path:
            drone.move(path[0])
    print()


pygame.init()

w, h = 1600, 1200
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Fly-in')
clock = pygame.time.Clock()

assets.load_assets(Path('assets'))
bg_rect = assets.IMG['bg'].get_rect(center=(800, 600))

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
    'Mouse 1: Next turn.',
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
ui_3 = pygame.font.Font.render(
    assets.FONT_BIG,
    'Space: Autoplay off.',
    True,
    (255, 127, 127),
    (0, 0, 0)
)
ui_3_rect = ui_3.get_rect(left=16, top=112)
ui_4 = pygame.font.Font.render(
    assets.FONT_BIG,
    'Space: Autoplay ON.',
    True,
    (127, 255, 127),
    (0, 0, 0)
)
ui_4_rect = ui_4.get_rect(left=16, top=112)


autoplay, autoplay_timer = False, 500
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
                execute_turn(zones, zones[end], drones)
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_SPACE]:
                autoplay = not autoplay
                autoplay_timer = 500

    screen.fill((100, 100, 100))
    screen.blit(assets.IMG['bg'], bg_rect)
    for x in links:
        x.draw(screen, cam)
    for x in zones.values():
        x.draw(screen, cam)
    for x in drones:
        x.update()
        x.draw(screen, cam)

    screen.blit(ui_1, ui_1_rect)
    screen.blit(ui_2, ui_2_rect)
    if autoplay:
        screen.blit(ui_4, ui_4_rect)
    else:
        screen.blit(ui_3, ui_3_rect)

    pygame.display.flip()
    clock.tick(60)

    if autoplay:
        autoplay_timer += clock.get_time()
        if autoplay_timer > 500:
            autoplay_timer -= 500
            execute_turn(zones, zones[end], drones)

# Optionally print total turn count for debugging.
# print('Turn count:', turncount)
pygame.quit()
