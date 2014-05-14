"""
State for levels.
"""
import pygame as pg
from .. import tools, setup, tilerender, collision
from .. import constants as c
from ..sprites import player, powerup, enemies


class Level(tools._State):
    def __init__(self, name):
        super(Level, self).__init__()
        self.name = name
        self.tmx_map = setup.TMX[name]

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.current_time = current_time
        self.state = c.NORMAL
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_map()

        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = self.make_level_surface(self.map_image)
        self.level_rect = self.level_surface.get_rect()
        self.player = self.make_player()
        self.sprites = self.make_sprites()
        self.blockers = self.make_blockers()
        self.item_boxes = self.make_item_boxes()
        self.stars = pg.sprite.Group()
        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.sprites,
                                                            self.blockers,
                                                            self.item_boxes,
                                                            self.stars)
        self.state_dict = self.make_state_dict()

    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return setup.SCREEN.get_rect(bottom=map_rect.bottom)

    def make_level_surface(self, map_image):
        """
        Create the surface all images blit to.
        """
        map_rect = map_image.get_rect()
        map_width = map_rect.width
        map_height = map_rect.height
        size = map_width, map_height

        return pg.Surface(size).convert()

    def make_player(self):
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'player start point':
                x = properties['x']
                y = properties['y']
                return player.Player(x, y)

    def make_sprites(self):
        sprite_group = pg.sprite.Group()

        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['type'] == 'enemy':
                name = properties['name']
                x = properties['x']
                y = properties['y']
                sprite_group.add(enemies.Enemy(x, y, name))

        return sprite_group

    def make_blockers(self):
        """
        Make the collideable blockers the player can collide with.
        """
        blockers = pg.sprite.Group()
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'blocker':
                x = properties['x']
                y = properties['y'] - 70
                width = height = 70
                blocker = pg.sprite.Sprite()
                blocker.rect = pg.Rect(x, y, width, height)
                blockers.add(blocker)

        return blockers

    def make_item_boxes(self):
        """
        Make item box sprite group.
        """
        item_boxes = pg.sprite.Group()
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'item box':
                x = properties['x']
                y = properties['y'] - 70
                width = height = 70
                box = powerup.ItemBox(x, y)
                item_boxes.add(box)

        return item_boxes

    def make_state_dict(self):
        """
        Make a dictionary of states the level can be in.
        """
        state_dict = {'normal': self.normal_mode}

        return state_dict

    def normal_mode(self, surface, keys, current_time, dt):
        """
        Update level normally.
        """
        self.player.update(keys, current_time, dt)
        self.sprites.update(current_time, dt)
        self.item_boxes.update(current_time)
        self.collision_handler.update(keys, current_time, dt)
        self.viewport_update()
        self.draw_level(surface)

    def update(self, surface, keys, current_time, dt):
        """
        Update state.
        """
        state_function = self.state_dict[self.state]
        state_function(surface, keys, current_time, dt)

    def viewport_update(self):
        """
        Update viewport so it stays centered on character,
        unless at edge of map.
        """
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def draw_level(self, surface):
        """
        Blit all images to screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)
        self.sprites.draw(self.level_surface)
        self.stars.draw(self.level_surface)
        self.item_boxes.draw(self.level_surface)
        surface.blit(self.level_surface, (0, 0), self.viewport)








