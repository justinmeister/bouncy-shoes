import pygame as pg
from .. import setup, tools
from .. import constants as c


class Enemy(pg.sprite.Sprite):
    """
    Basic enemy for game.
    """
    def __init__(self, x, y, name, direction=c.LEFT):
        super(Enemy, self).__init__()
        self.state_dict = self.make_state_dict()
        self.state = c.FREE_FALL
        self.walking_image_dict = self.make_walking_image_dict(name)
        self.direction = direction
        self.image_list = self.walking_image_dict[self.direction]
        self.index = 0
        self.timer = 0.0
        self.image = self.image_list[self.index]
        self.x_vel = 0
        self.y_vel = 0
        self.rect = self.image.get_rect(x=x, bottom=y)

    def make_state_dict(self):
        """
        Make the dictionary for the enemy states.
        """
        state_dict = {c.WALKING: self.walking_state,
                      c.FREE_FALL: self.free_fall_state}

        return state_dict

    def make_walking_image_dict(self, name):
        """
        Make the dictionary of the two
        walking image lists (one for each direction).
        """
        right_images = pg.transform.scale2x(setup.GFX[name])
        right_images = pg.transform.scale2x(right_images)
        left_images = pg.transform.flip(right_images, True, False)
        right_image_list = [tools.get_image(0, 0, 63, 84, right_images),
                            tools.get_image(64, 0, 63, 84, right_images)]
        left_image_list = [tools.get_image(0, 0, 64, 84, left_images),
                           tools.get_image(64, 0, 64, 84, left_images)]

        image_dict = {c.RIGHT: right_image_list,
                      c.LEFT: left_image_list}

        return image_dict

    def update(self, current_time, dt):
        state_function = self.state_dict[self.state]
        state_function(current_time, dt)

    def walking_state(self, current_time, dt):
        """
        Update enemy while it is walking.
        """
        self.image_list = self.walking_image_dict[self.direction]
        self.image = self.image_list[self.index]
        self.animate(current_time, dt)

    def animate(self, current_time, dt):
        """
        Animate sprite.
        """
        if (current_time - self.timer) > 300:
            self.timer = current_time
            if self.index < (len(self.image_list) - 1):
                self.index += 1
            else:
                self.index = 0

    def free_fall_state(self, *args):
        pass

    def enter_walking(self):
        """
        Transition into walking state.
        """
        self.state = c.WALKING
        self.y_vel = 0
        if self.direction == c.RIGHT:
            self.x_vel = c.SLOW_WALK_SPEED
        else:
            self.x_vel = c.SLOW_WALK_SPEED * -1

    def enter_fall(self):
        """
        Transition into falling state.
        """
        self.state = c.FREE_FALL
        self.y_vel = 0




