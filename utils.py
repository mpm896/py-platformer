from pathlib import Path

from constants import IMG_EXT
import pygame as pg

def load_images(dir: Path) -> tuple[pg.Surface]:
    """ Load multiple images. Returns of tuple of pygame Surface """
    imgs = []
    for img in dir.glob(f'*{IMG_EXT}'):
        surf = pg.image.load(img).convert_alpha()
        imgs.append(surf)
    return tuple(imgs)
