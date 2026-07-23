from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg

from constants import TILE_SIZE

if TYPE_CHECKING:
    from platformer import Game

class Tile:
    def __init__(self, img: pg.Surface, pos: pg.Vector2):
        self.img = img
        self.pos = pos * TILE_SIZE

class GroundTiles:
    def __init__(self, game: Game, tiles: list[Tile]):
        self.game = game
        self.tiles = tiles

    def add_tile(self, tile: Tile) -> None:
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile) -> None:
        if tile in self.tiles:
            self.tiles.remove(tile)

    def render(self) -> None:
        for tile in self.tiles:
            self.game.screen.blit(tile.img, (tile.pos.x, tile.pos.y))
