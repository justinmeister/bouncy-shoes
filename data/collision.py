"""
Handle game collisions.
"""
import math
import pygame as pg
from . import constants as c


class CollisionHandler(object):
    """
    Handles collisions between the player, enemies and game
    objects.
    """
    def __init__(self, player, sprites):
        self.player = player
        self.sprites = sprites


    def update(self, keys, current_time, dt):
        if self.player.state == c.WALKING:
            self.update_walking_player(keys, dt)
        elif self.player.state == c.JUMPING:
            self.update_jumping_player(keys, dt)

    def update_walking_player(self, keys, dt):
        """
        Move player when walking
        """
        if keys[pg.K_RIGHT]:
            self.player.direction = c.RIGHT
            self.player.x_vel += (c.MAX_SPEED - self.player.x_vel) * .1

        elif keys[pg.K_LEFT]:
            self.player.direction = c.LEFT
            self.player.x_vel -= (c.MAX_SPEED + self.player.x_vel) * .1
        else:
            if self.player.x_vel > 0:
                self.player.x_vel += (0 - self.player.x_vel) * .1
            elif self.player.x_vel < 0:
                self.player.x_vel += (0 - self.player.x_vel) * .1


        self.player.rect.x += self.player.x_vel * dt

        if self.player.x_vel > 0:
            if self.player.x_vel <= 25.0:
                self.player.state = c.STANDING
                self.player.x_vel = 0
        else:
            if self.player.x_vel >= -25.0:
                self.player.state = c.STANDING

    def update_jumping_player(self, keys, dt):
        """
        Move player while jumping
        """
        self.player.rect.x += self.player.x_vel * dt
        self.player.rect.y += self.player.y_vel * dt
        self.player.y_vel += c.GRAVITY * dt

