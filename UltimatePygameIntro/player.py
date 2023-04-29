import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.jump_image = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.frames = [walk1, walk2]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(80, settings.HORIZON))
        self.player_gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.bottom += self.player_gravity
        if self.rect.bottom >= settings.HORIZON:
            self.rect.bottom = settings.HORIZON

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= settings.HORIZON:
            self.player_gravity = -22
            self.jump_sound.play()

    def animation_state(self):
        if self.rect.bottom < settings.HORIZON:
            self.image = self.jump_image
            return
        self.frame_index += 0.1
        self.frame_index = (
            0 if self.frame_index > len(self.frames) else self.frame_index
        )
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
