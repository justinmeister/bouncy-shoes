"""
Main controllable player.
"""

import pygame as pg
from .. import tools, setup
from .. import constants as c


class Player(pg.sprite.Sprite):
    """
    User controlled player.
    """
    def __init__(self):
        super(Player, self).__init__()
        self.get_image = tools.get_image
        self.state_dict = self.make_state_dict()
        self.state = c.STANDING
        self.walking_image_dict = self.make_walking_image_dict()
        self.standing_image_dict = self.make_standing_image_dict()
        self.index = 0
        self.timer = 0.0
        self.direction = c.RIGHT
        self.x_vel = 0
        self.y_vel = 0
        self.image = self.standing_image_dict[self.direction]
        self.rect = self.image.get_rect(y=535)

    def make_state_dict(self):
        """
        Make the dictionary of state methods for player.
        """
        state_dict = {c.STANDING: self.standing,
                      c.WALKING: self.walking}
        return state_dict

    def standing(self, keys, current_time):
        """
        State when player is still.
        """
        self.image = self.standing_image_dict[self.direction]

        if keys[pg.K_RIGHT]:
            self.index = 0
            self.direction = c.RIGHT
            self.state = c.WALKING
            self.timer = current_time
        elif keys[pg.K_LEFT]:
            self.index = 0
            self.direction = c.LEFT
            self.state = c.WALKING
            self.timer = current_time

    def walking(self, keys, current_time):
        """
        State when player is walking.
        """
        self.image_list = self.walking_image_dict[self.direction]
        self.image = self.image_list[self.index]

        if (current_time - self.timer) > 100:
            self.timer = current_time
            if self.index < (len(self.image_list) - 1):
                self.index += 1
            else:
                self.index = 0

        if keys[pg.K_RIGHT]:
            self.direction = c.RIGHT
        elif keys[pg.K_LEFT]:
            self.direction = c.LEFT





    def make_walking_image_dict(self):
        """
        Make the list of walking animation images.
        """
        sprite_sheet = setup.GFX['p1_walking']

        right_images = self.make_walking_image_list(sprite_sheet)
        left_images = self.make_walking_image_list(sprite_sheet, True)

        walking_dict = {c.RIGHT: right_images,
                        c.LEFT: left_images}

        return walking_dict

    def make_walking_image_list(self, sprite_sheet, reverse_images=False):
        """
        Return a list of images for walking animation.
        """
        coord = []
        for y in range(2):
            for x in range(6):
                coord.append((x, y))

        walking_images = []
        for pos in coord:
            width = 72
            height = 97
            x = pos[0] * width
            y = pos[1] * height
            walking_images.append(self.get_image(x, y,
                                                 width, height,
                                                 sprite_sheet))
        walking_images.pop(-1)

        if reverse_images:
            flipped_images = []
            for image in walking_images:
                flipped_images.append(pg.transform.flip(image, True, False))
            return flipped_images
        else:
            return walking_images

    def make_standing_image_dict(self):
        """
        Make the list of the standing pose images.
        """
        right_image = setup.GFX['p1_stand']
        left_image = pg.transform.flip(right_image, True, False)

        return {c.RIGHT: right_image,
                c.LEFT: left_image}

    def update(self, keys, current_time):
        state_function = self.state_dict[self.state]
        state_function(keys, current_time)


