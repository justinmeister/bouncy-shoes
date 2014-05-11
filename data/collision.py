"""
Handle game collisions.
"""

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


    def update(self, keys, current_time):
        if self.player.state == c.WALKING:
            self.update_walking_player(keys)

    def update_walking_player(self, keys):
        """
        Move player when walking
        """
        if keys[pg.K_RIGHT]:
            self.player.direction = c.RIGHT
            if self.player.x_vel < c.MAX_SPEED:
                self.player.x_vel += c.ACCELERATION
        elif keys[pg.K_LEFT]:
            self.player.direction = c.LEFT
            if self.player.x_vel > (c.MAX_SPEED * -1):
                self.player.x_vel += (c.ACCELERATION * -1)
        else:
            if self.player.x_vel > 0:
                self.player.x_vel -= c.ACCELERATION
            elif self.player.x_vel < 0:
                self.player.x_vel -= (c.ACCELERATION * -1)

        self.player.rect.x += self.player.x_vel
