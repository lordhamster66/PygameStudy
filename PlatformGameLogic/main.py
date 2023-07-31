import pygame
import settings
from level import Level

pygame.init()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

level = Level()

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        screen.fill(settings.BG_COLOR)
        level.run()

        pygame.display.update()
        clock.tick(settings.FPS)
