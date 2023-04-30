import pygame

import settings


class Camera(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.screen = pygame.display.get_surface()
        screen_width = self.screen.get_size()[0]
        screen_height = self.screen.get_size()[1]

        self.half_w = screen_width // 2
        self.half_h = screen_height // 2
        self.offset = pygame.math.Vector2(0, 0)

        self.box_camera = pygame.Rect(
            settings.CAMERA_BORDERS['left'],
            settings.CAMERA_BORDERS['top'],
            screen_width
            - settings.CAMERA_BORDERS['left']
            - settings.CAMERA_BORDERS['right'],
            screen_height
            - settings.CAMERA_BORDERS['top']
            - settings.CAMERA_BORDERS['bottom'],
        )

    def camera_draw(self):
        for sprite in self.sprites():
            self.screen.blit(sprite.image, sprite.rect.topleft - self.offset)

    def flow_player(self, player):
        target_offset = pygame.math.Vector2(
            player.rect.topleft[0] - self.half_w,
            player.rect.topleft[1] - self.half_h,
        )
        distance = target_offset - self.offset
        self.offset.x += distance.x // 30
        self.offset.y += distance.y // 30
        self.camera_draw()

    def box_limit_camera(self, player):
        if player.rect.left < self.box_camera.left:
            self.box_camera.left = player.rect.left
        elif player.rect.right > self.box_camera.right:
            self.box_camera.right = player.rect.right

        if player.rect.top < self.box_camera.top:
            self.box_camera.top = player.rect.top
        elif player.rect.bottom > self.box_camera.bottom:
            self.box_camera.bottom = player.rect.bottom

        self.offset.x = self.box_camera.x - settings.CAMERA_BORDERS['left']
        self.offset.y = self.box_camera.y - settings.CAMERA_BORDERS['top']
        self.camera_draw()
