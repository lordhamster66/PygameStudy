from random import choice

import pygame
import settings
from obstacle import Obstacle
from player import Player


class MainScreen(object):
    def __init__(self):
        self.logo_image = pygame.image.load(
            'graphics/player/player_stand.png'
        ).convert_alpha()
        self.logo_image = pygame.transform.scale2x(self.logo_image)
        self.logo_rect = self.logo_image.get_rect(center=(400, 200))
        self.intro_text_color = (111, 196, 169)
        self.game_name = font.render('Pixel Runner', False, self.intro_text_color)
        self.game_name_rect = self.game_name.get_rect(center=(400, 80))

        self.game_message = font.render(
            'Press space to run', False, self.intro_text_color
        )
        self.game_message_rect = self.game_message.get_rect(center=(400, 320))

    def run(self):
        obstacles.empty()
        screen.fill((94, 129, 162))
        screen.blit(self.logo_image, self.logo_rect)
        screen.blit(self.game_name, self.game_name_rect)
        if score:
            display_score(f'Your score: {score}', self.intro_text_color, (400, 320))
        else:
            screen.blit(self.game_message, self.game_message_rect)


class Game(object):
    def __init__(self):
        self.sky_surf = pygame.image.load('graphics/sky.png').convert()
        self.ground_surf = pygame.image.load('graphics/ground.png').convert()

    def run(self):
        screen.blit(self.sky_surf, (0, 0))
        screen.blit(self.ground_surf, (0, settings.HORIZON))
        score = (pygame.time.get_ticks() - start_time) // 1000
        display_score(f'Score: {score}', (64, 64, 64), (400, 40))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()

        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            game_over()


def display_score(score_str, color, pos):
    score_surf = font.render(score_str, False, color)
    score_rect = score_surf.get_rect(center=pos)
    screen.blit(score_surf, score_rect)


def game_over():
    pygame.event.post(pygame.event.Event(settings.GAME_OVER_EVENT))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Runner")
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/Pixeltype.ttf', 50)
    bgm = pygame.mixer.Sound('audio/music.wav')
    bgm.play(loops=-1)

    player = pygame.sprite.GroupSingle(Player())
    obstacles = pygame.sprite.Group()

    score = 0
    start_time = 0
    pygame.time.set_timer(settings.OBSTACLE_SPAWN_EVENT, 1500)

    main_screen = MainScreen()
    game = Game()

    game_activate = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == settings.GAME_OVER_EVENT:
                game_activate = False
                start_time = pygame.time.get_ticks()

            if game_activate:
                if event.type == settings.OBSTACLE_SPAWN_EVENT:
                    obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_activate = True

        if game_activate:
            game.run()
        else:
            main_screen.run()

        pygame.display.update()
        clock.tick(60) / 1000
