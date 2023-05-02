from typing import Any

import pygame

import settings
from utility.load_assets import load_animations_from_sprite_sheets


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_group, *groups) -> None:
        super().__init__(*groups)
        self.animations = load_animations_from_sprite_sheets(
            settings.PLAYER_VIRTUAL_GUY_PATH,
            32,
            32,
            scale2x=True,
        )

        self.collision_group = collision_group

        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = 16

        self.max_jump_count = 2
        self.jump_count = self.max_jump_count
        self.air_time = 0
        self.jump_cool_time = 300

        self.last_animation_state = None
        self.animation_index = 0
        self.animation_speed = 0.2
        self.animation_flip = False
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.reset_actions()

    def reset_actions(self):
        self.actions = {'jump': False, 'land': False}

    @property
    def animation_state(self):
        if self.direction.y < 0:
            if self.jump_count == 0:
                return 'double_jump'
            return 'jump'
        if self.direction.y > 1:  # should grater than gravity
            return 'fall'

        if self.direction.x != 0:
            return 'run'
        return 'idle'

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.animation_flip = False
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.animation_flip = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            cool_time = pygame.time.get_ticks() - self.air_time
            if self.jump_count > 0 and cool_time >= self.jump_cool_time:
                self.actions['jump'] = True
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
                    break
                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    break

    def check_v_collisions(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jump_count = self.max_jump_count
                    if self.last_animation_state == 'fall':
                        self.actions['land'] = True
                    break
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    break

    def animate(self):
        animation_name = self.animation_state
        if self.animation_flip:
            animation_name = f'{animation_name}_flip'
        animation_list = self.animations[animation_name]
        self.animation_index += self.animation_speed
        self.image = animation_list[int(self.animation_index % len(animation_list))]
        self.last_animation_state = self.animation_state

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.reset_actions()
        self.handle_input()
        self.move()
        self.animate()
        self.check_h_collisions()
        self.apply_gravity()
        self.check_v_collisions()
