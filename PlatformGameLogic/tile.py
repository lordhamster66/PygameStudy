import pygame
import settings


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.TILE_COLOR)
        self.rect = self.image.get_rect(topleft=pos)
