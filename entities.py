from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

import pygame as pg

from constants import *

if TYPE_CHECKING:
    from platformer import Game

class Square:
    def __init__(
            self,
            x: float,
            y: float,
            width: float,
            height: float,
            rot: int = 0,
            color: pg.Color = None,
            vel_x: int = 0,
            vel_y: int = 0,
            gravity: int = 0
        ):
        self.x = x  # X and Y position
        self.y = y
        self.vel_x = vel_x  # X and Y velocity
        self.vel_y = vel_y
        self.width = width  # Size - Width and Height
        self.height = height
        if color is not None:  # For initial dev, using drawn shapes with colors
            self.color = color
            self.surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
            self.surf.fill(self.color)
        self.rot = rot
        self.gravity = gravity  # Whether or not to apply gravity
        self.jumping = False

    def rect(self) -> pg.Rect:
        return pg.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
    
    def jump(self) -> None:
        self.vel_y = -5
        self.jumping = True

    def update_position(self, dist: float, dt: float, collide_rects: Iterable[pg.Rect]) -> None:
        self.x += dist * dt * self.vel_x
        self.check_collisions_x(collide_rects)

        # Enforce gravity
        if self.gravity:
            self.vel_y = min(5, self.vel_y + GRAVITY * dt)
        self.y += dist * dt *self.vel_y
        self.check_collisions_y(collide_rects)


    def check_collision(self, collide_rects: Iterable[pg.Rect]) -> pg.Rect | None:
        """
        Check for collisions. Takes an iterable of rects to check against and returns current collision rect or None if no collision.
        """
        self_rect = self.rect()
        # self_rect.center = (self.x, self.y)
        for rect in collide_rects:
            if self_rect.colliderect(rect):
                return rect
        return None
    
    def check_collisions_x(self, collide_rects: Iterable[pg.Rect]) -> None:
        """ Check horizontal collisions """
        rect = self.check_collision(collide_rects)
        
        if rect is not None:
            # if self_rect.right > rect.left:  # Moving to the right
            if self.vel_x > 0:
                self.x = rect.left - self.width / 2
            elif self.vel_x < 0:  # Moving to the left
                self.x = rect.right + self.width / 2
            self.vel_x = 0

    def check_collisions_y(self, collide_rects: Iterable[pg.Rect]) -> None:
        """ Check vertical collisions """
        rect = self.check_collision(collide_rects)
        if rect is not None:
            if self.vel_y > 0:
                self.y = rect.top - self.height / 2
                self.jumping = False
            elif self.vel_y < 0:
                self.y = rect.bottom + self.height / 2
            self.vel_y = 0

    def blit_rotate(self, screen: pg.Surface) -> None:
        """
        Blit rect with given rotation angle
        """
        new_surf = pg.transform.rotate(self.surf, self.rot)
        new_surf_rect = new_surf.get_rect()
        new_surf_rect.center = (self.x, self.y)
        screen.blit(new_surf, new_surf_rect)


class PhysicsEntity:
    def __init__(self, game: Game, pos: pg.Vector2, size: pg.Vector2, img: pg.Surface):
        self.game = game
        self.pos = pos  # CENTER OF RECT
        self.velocity = pg.Vector2(0, 0)
        self.action = ''
        self.set_action('idle')
        self.set_img(img, size)
        self.flip = False

    def rect(self) -> pg.Rect:
        """ Return a rect for the entity. REMINDER: self.pos is center, so the returned rect give the top-left coordinate """
        # INTEGER DIVISION TO AVOID STUTTERING, ESPECIALLY IF RECT SIZE IS ODD
        return pg.Rect(self.pos.x - self.size.x // 2, self.pos.y - self.size.y // 2, self.size.x, self.size.y)

    def set_action(self, action: str) -> None:
        """ Change the action state of the entity """
        if action != self.action:
            self.action = action

    def set_img(self, img: pg.Surface, size: pg.Vector2=pg.Vector2(0,0)) -> None:
        """ Change image """
        self.img = img.subsurface(img.get_bounding_rect())
        # visible_area = img.get_bounding_rect()
        # self.img = img.subsurface(visible_area)
        # if visible_area.width != size.x or visible_area.height != size.y:
        #     self.img = img.subsurface(visible_area)
        #     self.size = pg.Vector2(visible_area.width, visible_area.height)
        # else:
        #     self.img = img
        #     self.size = size


    def update_position(self, dist: float, collide_rects: Iterable[pg.Rect]) -> None:
        # Update X position, check left-right collisions
        self.pos.x += dist * self.game.dt * self.velocity.x
        self.check_collisions_x(collide_rects)

        # Enforce gravity, update Y position, check up-down collisions
        self.velocity.y = min(5, self.velocity.y + GRAVITY * self.game.dt)
        self.pos.y += dist * self.game.dt * self.velocity.y
        self.check_collisions_y(collide_rects)


    def check_collision(self, collide_rects: Iterable[pg.Rect]) -> pg.Rect | None:
        """
        Check for collisions. Takes an iterable of rects to check against and returns current collision rect or None if no collision.
        """
        self_rect = self.rect()
        for rect in collide_rects:
            if self_rect.colliderect(rect):
                return rect
        return None
    
    def check_collisions_x(self, collide_rects: Iterable[pg.Rect]) -> None:
        """ Check horizontal collisions """
        rect = self.check_collision(collide_rects)
        if rect is not None:
            if self.velocity.x > 0: # Moving to the right
                self.pos.x = rect.left - self.size.x / 2
            elif self.velocity.x < 0:  # Moving to the left
                self.pos.x = rect.right + self.size.x / 2
            self.velocity.x = 0

    def check_collisions_y(self, collide_rects: Iterable[pg.Rect]) -> None:
        """ Check vertical collisions """
        rect = self.check_collision(collide_rects)
        if rect is not None:
            if self.velocity.y > 0:
                self.pos.y = rect.top - self.size.y / 2
            elif self.velocity.y < 0:
                self.pos.y = rect.bottom + self.size.y / 2
            self.velocity.y = 0

    def blit(self) -> None:
        """
        Blit rect with given rotation angle
        """
        rect = self.img.get_bounding_rect()
        rect.center = (self.pos.x, self.pos.y)
        self.game.screen.blit(pg.transform.flip(self.img, self.flip, 0), rect)


class Player(PhysicsEntity):
    def __init__(self, game: Game, pos: pg.Vector2, size: pg.Vector2, animation: dict[str, tuple[pg.Surface]]):

        self.jumps: int = 1
        self.air_time: int = 0
        self.speed: int = BASE_SPEED
        self.animation: dict[str, tuple[pg.Surface]] = animation
        self.animation_idx: int = 0
        self.animation_speed = 10

        # Get proper size for rect
        self.rect_sizes = {}
        for anim in self.animation:
            height = max([img.get_bounding_rect().height for img in self.animation[anim]])
            self.rect_sizes[anim] = pg.Vector2(size.x, height)
    
        super().__init__(game, pos, size, self.animation['idle'][0])

    def jump(self):
        if self.jumps and self.air_time < 5:
            self.set_action('jump')
            self.velocity.y = -2.5
            self.jumps -= 1
            self.air_time = 5

    def animate(self) -> None:
        """ Update the animation frame """
        self.animation_idx += self.animation_speed * self.game.dt
        img = self.animation[self.action][int(self.animation_idx) % len(self.animation[self.action])]
        self.set_img(img)

    def _draw_rect(self) -> None:
        pg.draw.rect(self.game.screen, "red", self.rect())

    def update(self, collide_rects: Iterable[pg.Rect]):
        self.size = self.rect_sizes[self.action]
        
        self.update_position(self.speed, collide_rects)

        self.air_time += 1
        if self.velocity.y == 0:
            self.jumps = 1
            self.air_time = 0

            if self.velocity.x == 0 and not self.action == 'look_up' and not self.action == 'crouch':
                self.set_action('idle')
            elif self.velocity.x != 0:
                self.set_action('run')

    def render(self):
        if self.velocity.x > 0:
            self.flip = False
        elif self.velocity.x < 0:
            self.flip = True
        self.blit()
        self.animate()


class CollisionRects:
    def __init__(self, game: Game, rects: list[pg.Rect]):
        self.game = game
        self.rects = rects

    def add_rect(self, rect: pg.Rect) -> None:
        self.rects.append(rect)

    def remove_rect(self, rect: pg.Rect) -> None:
        if rect in self.rects:
            self.rects.remove(rect)

    def __iter__(self):
        return iter(self.rects)


class Bullets:
    def __init__(self):
        self.bullets = []
        self.bullet_rot_speed = BULLET_ROT_SPEED

    def add_bullet(self, bullet: Square) -> None:
        self.bullets.append(bullet)

    def remove_bullet(self, bullet: Square) -> None:
        self.bullets.remove(bullet)

    def update_positions(self, dist: float, dt: float, collide_rects: Iterable[pg.Rect]) -> None:
            for i in range(len(self.bullets) - 1, -1, -1):
                self.bullets[i].update_position(BULLET_SPEED, dt, collide_rects)

                # Remove bullets with ground collisions or off screen for now
                if self.bullets[i].x > SCREEN_WIDTH + self.bullets[i].width:
                    self.remove_bullet(self.bullets[i])
                elif self.bullets[i].x < -self.bullets[i].width:
                    self.remove_bullet(self.bullets[i])
                elif self.bullets[i].y + self.bullets[i].width >= SCREEN_HEIGHT - GROUND_HEIGHT:
                    self.remove_bullet(self.bullets[i])
                elif self.bullets[i].vel_x == 0 and self.bullets[i].vel_y == 0:
                    self.remove_bullet(self.bullets[i])

    def blit(self, screen: pg.Surface) -> None:
        for i in range(len(self.bullets) - 1, -1, -1):
            self.bullets[i].rot = (self.bullets[i].rot + self.bullet_rot_speed) % 360
            self.bullets[i].blit_rotate(screen)


