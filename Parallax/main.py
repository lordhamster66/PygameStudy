import math

import pygame

FPS = 60
SCREEN_SIZE = (800, 432)


screen = pygame.display.set_mode(SCREEN_SIZE, vsync=True)
pygame.display.set_caption("Parallax")
clock = pygame.time.Clock()


bg_images = []
bg_scrolls = []
for i in range(1, 6):
    bg_images.append(pygame.image.load(f"images/plx-{i}.png").convert_alpha())
    bg_scrolls.append(0)
bg_count = len(bg_images)
bg_width = bg_images[0].get_width()
bg_draw_count = math.ceil(SCREEN_SIZE[0] / bg_width) + 1


def draw_bg(bg_scrolls):
    for bg_index, bg in enumerate(bg_images):
        bg_scroll = bg_scrolls[bg_index]
        bg_scroll = 0 if abs(bg_scroll) >= bg_width else bg_scroll
        bg_scrolls[bg_index] = bg_scroll
        for i in range(-1, bg_draw_count):
            screen.blit(bg, ((i * bg_width) - bg_scroll, 0))
    return bg_scrolls


ground_image = pygame.image.load("images/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
ground_scroll = 0
ground_draw_count = math.ceil(SCREEN_SIZE[0] / ground_width) + 1


def draw_ground(ground_scroll):
    ground_scroll = 0 if abs(ground_scroll) >= ground_width else ground_scroll
    for i in range(-1, ground_draw_count):
        screen.blit(
            ground_image,
            ((i * ground_width) - ground_scroll, SCREEN_SIZE[1] - ground_height),
        )
    return ground_scroll


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        bg_scrolls = draw_bg(bg_scrolls)
        ground_scroll = draw_ground(ground_scroll)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ground_scroll += 15
            speed = 1
            for i in range(bg_count):
                bg_scrolls[i] += 10 * speed
                speed += 0.2
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ground_scroll -= 15
            speed = 1
            for i in range(bg_count):
                bg_scrolls[i] -= 10 * speed
                speed += 0.2

        pygame.display.update()
        clock.tick(FPS)
