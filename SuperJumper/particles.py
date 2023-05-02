import os
from typing import Any

import pygame

import settings
from utility.load_assets import load_particle_animation


class Particle(pygame.sprite.Sprite):
    def __init__(self, name, pos, auto_kill, *groups) -> None:
        super().__init__(*groups)
        self.name = name
        self.auto_kill = auto_kill
        self.animations = load_particle_animation(
            self.name,
            os.path.join(settings.PLAYER_PARTICLES_PATH, self.name),
            with_flip=True if self.name == 'run' else False,
        )
        self.animation_index = 0
        self.animation_flip = False
        self.image = self.animations[self.name][self.animation_index]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.animation_index += 0.2
        animation_list = self.animations[
            f'{self.name}_flip' if self.animation_flip else self.name
        ]
        self.image = animation_list[int(self.animation_index % len(animation_list))]
        if self.auto_kill and self.animation_index > len(animation_list):
            self.kill()
