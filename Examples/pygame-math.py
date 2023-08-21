import pygame
from pygame.math import clamp
from pygame.math import Vector2

FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    delta = 0
    v1 = Vector2(10, 20)
    v2 = Vector2(30, 40)
    surface = pygame.Surface((10, 10))
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, 10, 10), 1)

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clamps a numeric value so that it's no lower than min, and no higher than max.
        print(f'5 clamp in 0 and 10 is:{clamp(5, 0, 10)}')

        # Vector2
        # _ip means in place
        print(f'v1:{v1}')
        print(f'v2:{v2}')
        print(f'v1.dot(v2):{v1.dot(v2)}')
        print(f'v1.length():{v1.length()}')  # 返回向量的欧几里得长度
        print(f'v1.normalize():{v1.normalize()}')  # 返回一个与原向量方向相同的单位向量
        # 返回一个沿着两点之间的直线移动的向量
        print(f'v1.move_towards(v2, 0.1):{v1.move_towards(v2, 0.1)}')
        v1.move_towards_ip(v2, 10 * delta)  # 向量v1沿着两点之间的直线移动
        print(f'v1.lerp(v2, 0.1):{v1.lerp(v2, 0.1)}')
        print(f'v1.angle_to(v2):{v1.angle_to(v2)}')  # 返回两个向量之间的角度

        # draw
        # fill the screen with a color to wipe away anything from last frame
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), v1, 1, 1)
        pygame.draw.circle(screen, (255, 255, 255), v2, 1, 1)
        pygame.transform.rotate(surface, v1.angle_to(v2))
        screen.blit(surface, (v1.x - 5, v1.y - 5))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS
        # delta time in seconds since last frame, used for framerate-
        # independent physics.
        delta = clock.tick(FPS) / 1000.0
        print(f'delta:{delta}')

    pygame.quit()


if __name__ == '__main__':
    main()
