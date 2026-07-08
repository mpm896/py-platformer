from enum import StrEnum, auto
from typing import Iterable

import pygame as pg

from entities import Bullets, Square
from constants import *

# TO DO:
#   - Update with Game class

# class Direction(StrEnum):
#     UP = auto()
#     DOWN = auto()
#     LEFT = auto()
#     RIGHT = auto()

# Initialize pygame and main screen
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Add a couple of squares to implement collisions
ground_rect = pg.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), SCREEN_WIDTH, GROUND_HEIGHT)
platform_rects = [ground_rect,
             pg.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, 200, 100), 
             pg.Rect(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 - 50, 75, 150)]

# pygame setup
clock = pg.time.Clock()
dt = 0
running = True

# Initialize player squaree
player = Square(PLAYER_START[0], PLAYER_START[1], PLAYER_SIZE[0], PLAYER_SIZE[1], color="red", gravity=1)
active_direction_keys = []

# Bullets
bullets = Bullets()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP):
                if not player.jumping:
                    player.jump()
            if event.key in (pg.K_w, pg.K_UP, pg.K_s, pg.K_DOWN, pg.K_a, pg.K_LEFT, pg.K_d, pg.K_RIGHT):
                active_direction_keys.append(event.key)
            if event.key == pg.K_q:
                
                vel_x = 1
                vel_y = 0
                pos = (player.x + player.width / 2, player.y)
                if active_direction_keys:
                    if active_direction_keys[-1] in (pg.K_w, pg.K_UP):
                        pos = (player.x, player.y - player.height / 2)
                        vel_x, vel_y = 0, -1
                    elif active_direction_keys[-1] in (pg.K_s, pg.K_DOWN) and player.jumping:
                        pos = (player.x, player.y + player.height / 2)
                        vel_x, vel_y = 0, 1
                    elif active_direction_keys[-1] in (pg.K_a, pg.K_LEFT):
                        pos = (player.x - player.width / 2, player.y)
                        vel_x, vel_y = -1, 0
                bullets.add_bullet(Square(pos[0], pos[1], BULLET_SIZE[0], BULLET_SIZE[1], color="blue", vel_x=vel_x, vel_y=vel_y))
        if event.type == pg.KEYUP:
            if event.key in active_direction_keys:
                active_direction_keys.remove(event.key)
    
    # Fill screen with background
    screen.fill(BACKGROUND)
    
    # Manage player direction
    keys_pressed = pg.key.get_pressed()
    player.vel_x = (keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]) - (keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]) 

    if player.vel_x:
        player.rot = (player.rot + ROT_SPEED) % 360
    else:
        if (player.rot % 90 != 0):
            player.rot = (player.rot + ROT_SPEED) % 360


    # Draw ground
    pg.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Draw platforms
    for platform in platform_rects[1:]:
        pg.draw.rect(screen, "green", platform)

    # Update player
    player.update_position(BASE_SPEED, dt, platform_rects)
    player.blit_rotate(screen)

    # Update bullets
    bullets.update_positions(BULLET_SPEED, dt, platform_rects)
    bullets.blit(screen)
    
    # Update the display
    pg.display.flip()

    dt = clock.tick(FPS) / 1000
    
    if DEBUG:
        print(player.x, player.y)

pg.quit()

