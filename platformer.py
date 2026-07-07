import pygame as pg
from enum import StrEnum, auto
from typing import Iterable

# TO DO:
#   - Fix basic collisions

DEBUG = False

FPS = 60
BACKGROUND = (255,255,255)  # White
BROWN = (131, 101, 57)  # Brown
BASE_SPEED = 200
GROUND_HEIGHT = 100
GRAVITY = 12

# class Direction(StrEnum):
#     UP = auto()
#     DOWN = auto()
#     LEFT = auto()
#     RIGHT = auto()

# Initialize pygame and main screen
pg.init()
screen = pg.display.set_mode((1280, 720))
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

class SquareEntity:
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
        player.jumping = True

    def update_position(self, dist: float, collide_rects: Iterable[pg.Rect]) -> None:
        self.x += dist * self.vel_x
        self.check_collisions_x(collide_rects)

        # Enforce gravity
        if self.gravity:
            self.vel_y = min(5, self.vel_y + GRAVITY * dt)
        self.y += dist * self.vel_y
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
PLAYER_START = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - GROUND_HEIGHT)
PLAYER_SIZE = (32,32)
player = SquareEntity(PLAYER_START[0], PLAYER_START[1], PLAYER_SIZE[0], PLAYER_SIZE[1], color="red", gravity=1)
rot = 0
rot_speed = -5
active_direction_keys = []

# Bullets
bullets = []
BULLET_SIZE = (7,7)
bullet_rot_speed = -8
bullet_speed = 500

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
                continue
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
                bullet = SquareEntity(pos[0], pos[1], BULLET_SIZE[0], BULLET_SIZE[1], color="blue", vel_x=vel_x, vel_y=vel_y)
                bullets.append(bullet)
        if event.type == pg.KEYUP:
            if event.key in active_direction_keys:
                active_direction_keys.remove(event.key)
    
    # Fill screen with background
    screen.fill(BACKGROUND)
    
    # Manage player direction
    keys_pressed = pg.key.get_pressed()
    player.vel_x = (keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]) - (keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]) 

    if player.vel_x:
        player.rot = (player.rot + rot_speed) % 360
    else:
        if (player.rot % 90 != 0):
            player.rot = (player.rot + rot_speed) % 360

    # Spawn and manage bullets
    for i in range(len(bullets) - 1, -1, -1):
        bullets[i].rot = (bullets[i].rot + bullet_rot_speed) % 360
        bullets[i].blit_rotate(screen)
        bullets[i].update_position(bullet_speed * dt)

        # Remove bullets with ground collisions or off screen for now
        if bullets[i].x > SCREEN_WIDTH + bullets[i].width:
            bullets.remove(bullets[i])
        elif bullets[i].x < -bullets[i].width:
            bullets.remove(bullets[i])
        elif bullets[i].y + bullets[i].width >= SCREEN_HEIGHT - GROUND_HEIGHT:
            bullets.remove(bullets[i])

    # Draw ground
    pg.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Draw platforms
    for platform in platform_rects[1:]:
        pg.draw.rect(screen, "green", platform)

    # Update player
    player.update_position(BASE_SPEED * dt, platform_rects)
    player.blit_rotate(screen)
    

    # Update the display
    pg.display.flip()

    dt = clock.tick(FPS) / 1000
    
    if DEBUG:
        print(player.x, player.y)

pg.quit()

