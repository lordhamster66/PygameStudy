from random import randint

import pygame
import settings


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type='snail'):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        if type == 'snail':
            image_list = ['graphics/snail/snail1.png', 'graphics/snail/snail2.png']
            self.y = settings.HORIZON
        elif type == 'fly':
            image_list = ['graphics/Fly/Fly1.png', 'graphics/Fly/Fly2.png']
            self.y = 210
        else:
            raise Exception("Wrong obstacle type!")

        for i in image_list:
            self.frames.append(pygame.image.load(i).convert_alpha())

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self.y))

    def ai_logic(self):
        self.rect.x -= 4
        if self.rect.x <= -100:
            self.kill()

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.ai_logic()
        self.animation_state()
