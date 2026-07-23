from enum import StrEnum, auto
from typing import Iterable

import pygame as pg
from pytmx.util_pygame import load_pygame

from constants import (DEBUG, FPS, BACKGROUND, BROWN, 
                       SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, 
                       PLAYER_SIZE, PLAYER_START, PLAYER_SPRITES_DIR, 
                       TILEMAP_DIR, TILE_SIZE, TEST_TILEMAP
                )
from entities import Bullets, CollisionRects, Player, Square
from props import Prop, PropGroup
from tiles import Tile, GroundTiles
from utils import load_images

# TO DO:
#   - Move player rotation to the Square class

# class Direction(StrEnum):
#     UP = auto()
#     DOWN = auto()
#     LEFT = auto()
#     RIGHT = auto()

class Game:
    def __init__(self):
        # Initialize pygame and main screen
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Add a couple of squares to implement collisions
        self.ground_rect = pg.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), SCREEN_WIDTH, GROUND_HEIGHT)
        # self.platform_rects = [self.ground_rect,
        #             pg.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, 200, 100), 
        #             pg.Rect(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 - 50, 75, 150)]
        self.platform_rects = []

        # pygame setup
        self.clock = pg.time.Clock()
        self.dt = 0
        self.running = True

        self.active_direction_keys = []

        self.load_assets()
        self.setup()

    def load_assets(self) -> None:
        # Load player assets
        self.player_imgs: dict[str, tuple[pg.Surface]] = {}
        for action_dir in PLAYER_SPRITES_DIR.iterdir():
            if action_dir.is_dir():
                imgs: tuple[pg.Surface] = load_images(action_dir)
                self.player_imgs[action_dir.name] = imgs

    def setup(self) -> None:
        map = load_pygame(TILEMAP_DIR)

        props = []
        for prop in map.get_layer_by_name('props'):
            img = map.get_tile_image_by_gid(prop.gid)
            pos = pg.Vector2(prop.x, prop.y)
            props.append(Prop(img, pos))
        self.props = PropGroup(self, props)

        ground_tiles = []
        for x, y, img in map.get_layer_by_name('ground').tiles():
            ground_tiles.append(Tile(img, pg.Vector2(x, y)))
        self.ground_tiles = GroundTiles(self, ground_tiles)

        collision_rects = []
        for rect in map.get_layer_by_name('collisions'):
            collision_rects.append(pg.Rect(rect.x, rect.y, rect.width, rect.height))
        self.ground_rects = CollisionRects(self, collision_rects)

        for loc in map.get_layer_by_name('player_spawn'):
            self.player = Player(self, pg.Vector2(loc.x, loc.y), pg.Vector2(PLAYER_SIZE), self.player_imgs)


    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:

                    # Jump
                    if event.key == pg.K_SPACE:
                        if self.player.jumps:
                            self.player.jump()
                    
                    # Grab last movement key. Important for velocity of bullet
                    # if event.key in (pg.K_w, pg.K_UP, pg.K_s, pg.K_DOWN, pg.K_a, pg.K_LEFT, pg.K_d, pg.K_RIGHT):
                    #     self.active_direction_keys.append(event.key)

                    if event.key in (pg.K_UP, pg.K_w):
                        if self.player.velocity.x == 0:
                            self.player.set_action('look_up')

                    if event.key in (pg.K_DOWN, pg.K_s):
                        if self.player.velocity.x == 0:
                            self.player.set_action('crouch')

                # if pg.K_UP in self.active_direction_keys:
                #         self.player.set_action('look_up')

                    # Shoot bullet. Get proper direction and starting position of bullet w.r.t. player
                    # if event.key == pg.K_q:
                    #     vel_x = 1
                    #     vel_y = 0
                    #     pos = (self.player.x + self.player.width / 2, self.player.y)
                    #     if self.active_direction_keys:
                    #         if self.active_direction_keys[-1] in (pg.K_w, pg.K_UP):
                    #             pos = (self.player.x, self.player.y - self.player.height / 2)
                    #             vel_x, vel_y = 0, -1
                    #         elif self.active_direction_keys[-1] in (pg.K_s, pg.K_DOWN) and self.player.jumping:
                    #             pos = (self.player.x, self.player.y + self.player.height / 2)
                    #             vel_x, vel_y = 0, 1
                    #         elif self.active_direction_keys[-1] in (pg.K_a, pg.K_LEFT):
                    #             pos = (self.player.x - self.player.width / 2, self.player.y)
                    #             vel_x, vel_y = -1, 0
                    #     self.bullets.add_bullet(
                    #         Square(pos[0], pos[1], BULLET_SIZE[0], BULLET_SIZE[1], color="blue", vel_x=vel_x, vel_y=vel_y)
                    #     )

                if event.type == pg.KEYUP:
                    # if event.key in self.active_direction_keys:
                    #     self.active_direction_keys.remove(event.key)
                    if event.key in (pg.K_UP, pg.K_w, pg.K_DOWN, pg.K_s):
                            self.player.set_action('idle')
            
            
            # Manage player direction
            keys_pressed = pg.key.get_pressed()
            self.player.velocity.x = (keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]) - (keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]) 
            

            # if self.player.vel_x:
            #     self.player.rot = (self.player.rot + ROT_SPEED) % 360
            # else:
            #     if (self.player.rot % 90 != 0):
            #         self.player.rot = (self.player.rot + ROT_SPEED) % 360


            # Fill screen with background
            self.screen.fill(BACKGROUND)

            self.props.render()
            self.ground_tiles.render()

            # Update bullets
            # self.bullets.update_positions(BULLET_SPEED, self.dt, self.platform_rects)
            # self.bullets.blit(self.screen)

            # Update player
            self.player.update(self.ground_rects)
            self.player.render()
            
            # Update the display
            pg.display.flip()

            self.dt = self.clock.tick(FPS) / 1000
            
            if DEBUG:
                print(self.player.action)

        pg.quit()

if __name__ == '__main__':
    Game().run()