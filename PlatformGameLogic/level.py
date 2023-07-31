import pygame
import settings
from camera import Camera
from player import Player
from tile import Tile


class Level(object):
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()

        self.camera = Camera()
        self.activate_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.player = None

        self.setup()

    def setup(self):
        for row_index, row in enumerate(settings.LEVEL_MAP):
            for col_index, col in enumerate(row):
                x = col_index * settings.TILE_SIZE
                y = row_index * settings.TILE_SIZE
                if col == "X":
                    Tile((x, y), [self.camera, self.collision_group])
                elif col == "P":
                    self.player = Player(
                        (x, y),
                        self.collision_group,
                        [self.camera, self.activate_group],
                    )

    def run(self):
        self.activate_group.update()
        # self.camera.flow_player(self.player)
        self.camera.box_limit_camera(self.player)
