from typing import Any

import pygame

import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_group, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((settings.TILE_SIZE // 2, settings.TILE_SIZE))
        self.image.fill(settings.PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        self.collision_group = collision_group

        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = 16

        self.rest_jump_count()
        self.air_time = 0
        self.jump_cool_time = 300

    def rest_jump_count(self):
        self.jump_count = 2

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            cool_time = pygame.time.get_ticks() - self.air_time
            if self.jump_count > 0 and cool_time >= self.jump_cool_time:
                self.direction.y = -self.jump_speed
                self.jump_count -= 1
                self.air_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x += self.direction.x * self.speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def check_h_collisions(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right

    def check_v_collisions(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.rest_jump_count()
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.handle_input()
        self.move()
        self.check_h_collisions()
        self.apply_gravity()
        self.check_v_collisions()
