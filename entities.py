from typing import Iterable

import pygame as pg

from constants import *

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


