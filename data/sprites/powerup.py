import pygame as pg
from .. import tools, setup
from .. import constants as c


class ItemBox(pg.sprite.Sprite):
    """
    Item box for powerups.
    """
    def __init__(self, x, y):
        super(ItemBox, self).__init__()
        self.get_image = tools.get_image
        self.image_list = self.make_image_list()
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(x=x, bottom=y)
        self.state_dict = self.make_state_dict()
        self.state = c.NORMAL
        self.timer = 0.0
        self.first_half = True

    def make_image_list(self):
        """
        Make the list of images for item box animation.
        """
        spritesheet = setup.GFX['spritesheet1']
        image_list = []

        for i in range(3):
            x = 490 - (i * 70)
            y = 490
            width = 70
            height = 70
            image_list.append(self.get_image(x, y, width, height, spritesheet))

        return image_list

    def make_state_dict(self):
        """
        Make the state dictionary.
        """
        state_dict = {c.NORMAL: self.normal_state,
                      c.BUMPED: self.bumped_state,
                      c.OPENED: self.opened_state}

        return state_dict

    def update(self, current_time):
        """
        Update Item box based on state function.
        """
        state_function = self.state_dict[self.state]
        state_function(current_time)

    def normal_state(self, current_time):
        """
        Update when box in normal state.
        """
        self.animate(current_time)


    def animate(self, current_time):
        self.image = self.image_list[self.index]

        if self.first_half:
            if self.index == 0:
                if (current_time - self.timer) > 375:
                    self.index += 1
                    self.timer = current_time
            elif self.index < 2:
                if (current_time - self.timer) > 125:
                    self.index += 1
                    self.timer = current_time
            elif self.index == 2:
                if (current_time - self.timer) > 125:
                    self.index -= 1
                    self.first_half = False
                    self.timer = current_time
        else:
            if self.index == 1:
                if (current_time - self.timer) > 125:
                    self.index -= 1
                    self.first_half = True
                    self.timer = current_time


    def bumped_state(self):
        """
        Update when box in bumped state.
        """
        pass

    def opened_state(self):
        """
        Update when box in opened state.
        """
        pass



