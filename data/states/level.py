"""
State for levels.
"""
import pygame as pg
from .. import tools, setup, tilerender, collision
from .. import constants as c
from ..sprites import player


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
        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.sprites)
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
        return player.Player()

    def make_sprites(self):
        return pg.sprite.Group()

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
        self.player.update(keys, current_time)
        self.sprites.update(current_time)
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
        surface.blit(self.level_surface, (0, 0), self.viewport)








