import collections
import os

import pygame


def load_animations(path, with_flip=True):
    animations = collections.defaultdict(list)
    for p, _, images in os.walk(path):
        if not images:
            continue
        animation_name = os.path.basename(p)
        for image in images:
            sprite = pygame.image.load(os.path.join(p, image)).convert_alpha()
            animations[animation_name].append(sprite)
            if with_flip:
                sprite_flip = pygame.transform.flip(sprite, True, False)
                animations[f'{animation_name}_flip'].append(sprite_flip)
    return animations


def load_particle_animation(name, path, with_flip=True):
    particle_animation = collections.defaultdict(list)
    for image_name in os.listdir(path):
        image_file = os.path.join(path, image_name)
        sprite = pygame.image.load(image_file).convert_alpha()
        particle_animation[name].append(sprite)
        if with_flip:
            sprite_flip = pygame.transform.flip(sprite, True, False)
            particle_animation[f'{name}_flip'].append(sprite_flip)
    return particle_animation


def load_animations_from_sprite_sheets(
    path,
    width,
    height,
    scale2x=False,
    with_flip=True,
):
    animations = collections.defaultdict(list)
    for image_name in os.listdir(path):
        animation_name, _ = os.path.splitext(image_name)
        image_file = os.path.join(path, image_name)
        sprite_sheet = pygame.image.load(image_file).convert_alpha()
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprite = pygame.transform.scale2x(surface) if scale2x else surface
            animations[animation_name].append(sprite)
            if with_flip:
                sprite_flip = pygame.transform.flip(sprite, True, False)
                animations[f'{animation_name}_flip'].append(sprite_flip)
    return animations
