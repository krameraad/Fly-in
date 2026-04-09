from pathlib import Path

import pygame


IMG: dict[str, pygame.Surface] = {}


def load_assets(path: Path) -> dict[str, pygame.Surface]:
    for f in path.iterdir():
        if f.suffix == '.png':
            IMG.update(
                {
                    str(f).removeprefix('assets/').removesuffix('.png'):
                        pygame.image.load(f).convert_alpha()
                }
            )
