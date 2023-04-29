from random import choice
from random import randint

import pygame

# some variables
dt = 0
ground_y = 300
player_gravity = 0
game_activate = False
start_time = 0


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()


font = pygame.font.Font('font/Pixeltype.ttf', 50)


sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(800, ground_y))


# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(400, 200))


intro_text_color = (111, 196, 169)
game_name = font.render('Pixel Runner', False, intro_text_color)
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = font.render('Press space to run', False, intro_text_color)
game_message_rect = game_message.get_rect(center=(400, 320))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.jump_image = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.frames = [walk1, walk2]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(80, ground_y))
        self.player_gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.bottom += self.player_gravity
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= ground_y:
            self.player_gravity = -20
            self.jump_sound.play()

    def animation_state(self):
        if self.rect.bottom < ground_y:
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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type='snail'):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        if type == 'snail':
            image_list = ['graphics/snail/snail1.png', 'graphics/snail/snail2.png']
            y_pos = ground_y
        elif type == 'fly':
            image_list = ['graphics/Fly/Fly1.png', 'graphics/Fly/Fly2.png']
            y_pos = 210

        for i in image_list:
            self.frames.append(pygame.image.load(i).convert_alpha())

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def ai_logic(self):
        self.rect.x -= 4
        if self.rect.x <= -100:
            self.kill()

    def animation_state(self):
        pass

    def update(self):
        self.ai_logic()
        self.animation_state()


class GameState(object):
    def __init__(self):
        self.dt = 0
        self.game_activate = False
        self.score = 0
        self.player_single = pygame.sprite.GroupSingle()
        self.player_single.add(Player())
        self.obstacles = pygame.sprite.Group()
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

    def display_score(self, score_str, color, pos):
        score_surf = font.render(score_str, False, color)
        score_rect = score_surf.get_rect(center=pos)
        screen.blit(score_surf, score_rect)

    def gameplay(self):
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, ground_y))
        self.score = (pygame.time.get_ticks() - start_time) // 1000
        self.display_score(f'Score: {self.score}', (64, 64, 64), (400, 40))
        self.player_single.draw(screen)
        self.player_single.update()
        self.obstacles.draw(screen)
        self.obstacles.update()

    def main_screen(self):
        self.obstacles.empty()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if self.score:
            self.display_score(
                f'Your score: {self.score}', intro_text_color, (400, 320)
            )
        else:
            screen.blit(game_message, game_message_rect)

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if self.game_activate:
                if event.type == self.obstacle_timer:
                    self.obstacles.add(
                        Obstacle(choice(['fly', 'snail', 'snail', 'snail']))
                    )
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_activate = True

        if self.game_activate:
            self.gameplay()
        else:
            self.main_screen()

        pygame.display.update()
        self.dt = clock.tick(60) / 1000


game_state = GameState()


while True:
    game_state.tick()
