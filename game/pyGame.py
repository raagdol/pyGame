'''
Created on 2023.08.16

@author: raagdol
'''

import sys
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Avoid Obstacles")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = SURFACE.get_width() // 2
        self.rect.bottom = SURFACE.get_height() - 10
        self.speed = 5

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, SURFACE.get_width() - self.rect.width))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(20, 100), 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SURFACE.get_width() - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SURFACE.get_height():
            self.kill()

def show_game_over_screen(score):
    sysfont = pygame.font.SysFont(None, 72)
    game_over_image = sysfont.render("GAME OVER", True, (255, 0, 0))
    score_image = sysfont.render("Score: {}".format(score // 10), True, (255, 255, 255))
    SURFACE.fill((0, 0, 0))

    game_over_rect = game_over_image.get_rect(center=(SURFACE.get_width() // 2, SURFACE.get_height() // 2 - 50))
    score_rect = score_image.get_rect(center=(SURFACE.get_width() // 2, SURFACE.get_height() // 2 + 50))

    SURFACE.blit(game_over_image, game_over_rect)
    SURFACE.blit(score_image, score_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def main():
    sysfont = pygame.font.SysFont(None, 36)
    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    clock = pygame.time.Clock()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if random.randint(0, 100) < 10:
            new_obstacle = Obstacle()
            obstacles.add(new_obstacle)
            all_sprites.add(new_obstacle)

        obstacles.update()

        SURFACE.fill((0, 0, 0))

        collisions = pygame.sprite.spritecollide(player, obstacles, False)
        if collisions:
            show_game_over_screen(score)
            pygame.time.delay(1500)  # 잠시 기다림
            return

        all_sprites.draw(SURFACE)

        score += 1
        score_image = sysfont.render("Score: {}".format(score // 10), True, (255, 255, 255))
        SURFACE.blit(score_image, (10, 10))

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()