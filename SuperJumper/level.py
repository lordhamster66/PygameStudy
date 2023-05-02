import pygame

import settings
from camera import Camera
from particles import Particle
from player import Player
from tile import Tile


class Level(object):
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()

        self.camera = Camera()
        self.activate_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.player = None
        self.run_particle = None

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

    def update_particles(self):
        if self.player.animation_state == 'run' and not self.run_particle:
            self.run_particle = Particle(
                'run',
                self.player.rect.midbottom,
                False,
                [self.activate_group, self.camera],
            )
        elif self.player.animation_state == 'run' and self.run_particle:
            if self.player.direction.x > 0:
                self.run_particle.rect.bottomright = self.player.rect.bottomleft
                self.run_particle.animation_flip = False
            elif self.player.direction.x < 0:
                self.run_particle.rect.bottomleft = self.player.rect.bottomright
                self.run_particle.animation_flip = True
        elif self.player.animation_state != 'run' and self.run_particle:
            self.run_particle.kill()
            self.run_particle = None

        if self.player.actions['jump']:
            Particle(
                'jump',
                self.player.rect.midbottom,
                True,
                [self.activate_group, self.camera],
            )
        if self.player.actions['land']:
            Particle(
                'land',
                self.player.rect.midbottom,
                True,
                [self.activate_group, self.camera],
            )

    def run(self):
        self.activate_group.update()
        self.update_particles()
        # self.camera.flow_player(self.player)
        self.camera.box_limit_camera(self.player)
