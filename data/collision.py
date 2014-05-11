"""
Handle game collisions.
"""

import pygame as pg
from . import constants


class CollisionHandler(object):
    """
    Handles collisions between the player, enemies and game
    objects.
    """
    def __init__(self, player, sprites):
        self.player = player
        self.sprites = sprites

    def update(self):
        pass