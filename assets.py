from pathlib import Path

import pygame


IMG: dict[str, pygame.Surface] = {}

pygame.font.init()
FONT: pygame.font.Font = pygame.font.Font(
    'font/lovely-pixels.otf', size=24)
FONT_BIG: pygame.font.Font = pygame.font.Font(
    'font/lovely-pixels.otf', size=48)


def load_assets(path: Path) -> None:
    for f in path.iterdir():
        if f.suffix == '.png':
            IMG.update({
                str(f).removeprefix('assets/').removesuffix('.png'):
                pygame.image.load(f).convert_alpha()
            })
