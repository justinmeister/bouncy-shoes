"""
Handle game collisions.
"""
import math
import pygame as pg
from . import constants as c
from .sprites import powerup


class CollisionHandler(object):
    """
    Handles collisions between the player, enemies and game
    objects.
    """
    def __init__(self, player, sprites, blockers, item_boxes, stars):
        self.player = player
        self.sprites = sprites
        self.stars = stars
        self.blockers = blockers
        self.item_boxes = item_boxes
        self.state_dict = self.make_state_dict()
        self.current_time = 0.0

    def make_state_dict(self):
        """
        Make dictionary for collision handler states.
        """
        state_dict = {c.WALKING: self.update_walking_player,
                      c.FREE_FALL: self.update_player_in_freefall,
                      c.STANDING: self.update_walking_player,
                      c.BOUNCY: self.update_player_in_freefall}

        return state_dict

    def update(self, keys, current_time, dt):
        state_function = self.state_dict[self.player.state]
        state_function(keys, dt, current_time)

    def update_walking_player(self, keys, dt, current_time):
        """
        Move player when walking
        """
        self.current_time = current_time
        self.adjust_horizontal_motion(keys)
        self.player.rect.x += self.player.x_vel * dt
        self.check_for_collision(False, True)

        if self.player.x_vel > 0:
            if self.player.x_vel <= 25.0:
                self.player.enter_standing()
        else:
            if self.player.x_vel >= -25.0:
                self.player.enter_standing()

        self.check_for_ground()
        self.adjust_item_box_position(dt)
        self.adjust_powerup_position(dt)

    def update_player_in_freefall(self, keys, dt, current_time):
        """
        Move player while jumping
        """
        self.current_time = current_time
        self.adjust_horizontal_motion(keys, False)

        self.player.rect.x += self.player.x_vel * dt
        self.check_for_collision(False, True)
        self.player.rect.y += self.player.y_vel * dt
        self.check_for_collision(True)

        self.player.y_vel += c.GRAVITY * dt

        self.adjust_item_box_position(dt)
        self.adjust_powerup_position(dt)


    def check_for_collision(self, vertical=False, horiz=False):
        """
        Check for ground and other blockers while in air.
        """
        blocker = pg.sprite.spritecollideany(self.player, self.blockers)
        item_box = pg.sprite.spritecollideany(self.player, self.item_boxes)
        bouncy_star = pg.sprite.spritecollideany(self.player, self.stars)

        if blocker and vertical:
            self.adjust_blocker_collision(blocker, True)
        elif blocker and horiz:
            self.adjust_blocker_collision(blocker, False, True)

        if item_box and vertical:
            self.adjust_item_box_collision(item_box, True)
        elif item_box and horiz:
            self.adjust_item_box_collision(item_box, False, True)

        if bouncy_star:
            bouncy_star.kill()
            self.player.enter_bouncy_state(self.current_time)

    def adjust_blocker_collision(self, blocker, vertical=False, horiz=False):
        """
        Adjust for collision with blockers.
        """
        if vertical:
            if self.player.y_vel > 0:
                self.player.rect.bottom = blocker.rect.top
                if self.player.state == c.BOUNCY:
                    self.player.y_vel = c.START_JUMP_VEL
                else:
                    self.player.enter_walking()
            elif self.player.y_vel < 0:
                self.player.rect.top = blocker.rect.bottom
                self.player.y_vel = 0
        elif horiz:
            if self.player.x_vel > 0:
                self.player.rect.right = blocker.rect.left
            elif self.player.x_vel < 0:
                self.player.rect.left = blocker.rect.right

    def adjust_item_box_collision(self, item_box, vertical=False, horiz=False):
        """
        Adjust for collision with item boxes.
        """
        if vertical:
            if self.player.y_vel > 0:
                self.player.rect.bottom = item_box.rect.top
                if self.player.state == c.BOUNCY:
                    self.player.y_vel = c.START_JUMP_VEL
                else:
                    self.player.enter_walking()
            elif self.player.y_vel < 0:
                self.player.rect.top = item_box.rect.bottom
                self.player.y_vel = 0
                if item_box.state == c.NORMAL:
                    item_box.enter_bump()
        if horiz:
            if self.player.x_vel > 0:
                self.player.rect.right = item_box.rect.left
            elif self.player.x_vel < 0:
                self.player.rect.left = item_box.rect.right

    def check_for_ground(self):
        """
        Check for ground when walking off ledge.
        """
        self.player.rect.y += 1

        collideables = pg.sprite.Group(self.blockers, self.item_boxes)

        if not pg.sprite.spritecollideany(self.player, collideables):
            self.player.enter_fall()

        self.player.rect.y -= 1

    def adjust_horizontal_motion(self, keys, on_ground=True):
        """
        Adjust horizontal motion.
        """
        if keys[pg.K_RIGHT]:
            self.player.direction = c.RIGHT
            self.player.x_vel += (self.player.max_speed - self.player.x_vel) * .1

        elif keys[pg.K_LEFT]:
            self.player.direction = c.LEFT
            self.player.x_vel -= (self.player.max_speed + self.player.x_vel) * .1

        else:
            if on_ground:
                self.ground_deceleration()


    def ground_deceleration(self):
        """
        Slow down character on ground.
        """
        if self.player.x_vel > 0:
            self.player.x_vel += (0 - self.player.x_vel) * .1
        elif self.player.x_vel < 0:
            self.player.x_vel += (0 - self.player.x_vel) * .1

    def adjust_item_box_position(self, dt):
        """
        Adjust item_box position based on y_vel.
        """
        for item_box in self.item_boxes:
            if item_box.state == c.BUMPED:
                item_box.y_vel += c.BUMP_GRAVITY * dt
                item_box.rect.y += item_box.y_vel * dt
                if item_box.rect.bottom > item_box.start_y:
                    item_box.enter_opened_state()
                    x = item_box.rect.centerx
                    y = item_box.rect.top
                    bouncy_star = powerup.BouncyStar(x, y)
                    self.stars.add(bouncy_star)

    def adjust_powerup_position(self, dt):
        """
        Adjust the position of star powerups based on y_vel.
        """
        for star in self.stars:
            if star.state == c.REVEAL:
                star.y_vel += c.BUMP_GRAVITY * dt
                star.rect.y += star.y_vel * dt
                if star.rect.bottom > star.start_y:
                    star.enter_revealed_state()





