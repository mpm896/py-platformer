from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from platformer import Game

class Prop:
    def __init__(self, img: pg.Surface, pos: pg.Vector2):
        self.img = img
        self.pos = pos


class PropGroup:
    def __init__(self, game: Game, props: list[Prop]):
        self.game = game
        self.props = props

    def add_prop(self, prop: Prop) -> None:
        self.props.append(prop)

    def remove_prop(self, prop: Prop) -> None:
        if prop in self.props:
            self.props.remove(prop)

    def render(self) -> None:
        for prop in self.props:
            self.game.screen.blit(prop.img, (prop.pos.x, prop.pos.y))

