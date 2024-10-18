# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Airplane Wars')

# Load the background map
try:
    background = pygame.image.load('resources/image/background.png')
except pygame.error as e:
    print(f"Cannot load background image: {e}")
    exit()

background_y = 0  # Position verticale du premier fond

scroll_speed = 0.5  # Vitesse de défilement


menu_font = pygame.font.SysFont(None, 48) 

def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, (128,128,128))
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def main_menu():
    menu_running = True
    background_y = 0 
    scroll_speed = 2 

    while menu_running:
        background_y += scroll_speed
        if background_y >= SCREEN_HEIGHT:
            background_y = 0

        screen.blit(background, (0, background_y))
        screen.blit(background, (0, background_y - SCREEN_HEIGHT))

        title_text = menu_font.render('Airplane Wars', True, (128,128,128))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        start_rect = draw_text('Start Game', menu_font, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        quit_rect = draw_text('Quit', menu_font, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

main_menu()

# Load the picture of the plane
try:
    plane_img = pygame.image.load('resources/image/shoot.png')
except pygame.error as e:
    print(f"Cannot load plane image: {e}")
    exit()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [plane_img.subsurface(rect).convert_alpha() for rect in player_rect]
        self.rect = player_rect[0].copy()
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.top < SCREEN_HEIGHT - self.rect.height:
            self.rect.top += self.speed

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.left < SCREEN_WIDTH - self.rect.width:
            self.rect.left += self.speed

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

# Define the Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

# Define player parameters
player_rect = [
    pygame.Rect(0, 99, 102, 126),
    pygame.Rect(165, 360, 102, 126),
    pygame.Rect(165, 234, 102, 126),
    pygame.Rect(330, 624, 102, 126),
    pygame.Rect(330, 498, 102, 126),
    pygame.Rect(432, 624, 102, 126)
]
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# Load bullet image and sound
try:
    bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
    bullet_sound.set_volume(0.3)
except pygame.error as e:
    print(f"Cannot load bullet sound: {e}")
    exit()

bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# Load enemy images and sound
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
try:
    enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
    enemy1_down_sound.set_volume(0.3)
except pygame.error as e:
    print(f"Cannot load enemy down sound: {e}")
    exit()

enemy1_down_imgs = [
    plane_img.subsurface(pygame.Rect(267, 347, 57, 43)),
    plane_img.subsurface(pygame.Rect(873, 697, 57, 43)),
    plane_img.subsurface(pygame.Rect(267, 296, 57, 43)),
    plane_img.subsurface(pygame.Rect(930, 697, 57, 43))
]

# Load game over image and sound
try:
    game_over = pygame.image.load('resources/image/gameover.png')
    game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
    game_over_sound.set_volume(0.3)
except pygame.error as e:
    print(f"Cannot load game over resources: {e}")
    exit()

# Initialize game variables
clock = pygame.time.Clock()
running = True
shoot_frequency = 0
enemy_frequency = 0
enemies1 = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
score = 0
player_down_index = 16

# Main game loop
while running:
    # Control the maximum frame rate
    clock.tick(45)
    background_y += scroll_speed

    # Repositionner les backgrounds lorsqu'ils sortent de l'écran
    if background_y >= SCREEN_HEIGHT:
        background_y = 0

    # Dessiner les backgrounds
    screen.blit(background, (0, background_y)) 
    screen.blit(background, (0, background_y - background.get_height()))  # Utilise la hauteur réelle de l'image

    # Control the shooting frequency
    if shoot_frequency % 15 == 0:
        bullet_sound.play()
        player.shoot(bullet_img)
    shoot_frequency += 1
    if shoot_frequency >= 15:
        shoot_frequency = 0

    # Move player
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.move_up()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.move_down()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.move_left()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.move_right()

    # Move bullets and remove if out of screen
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # Draw player
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # Spawn enemies
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # Move enemies and check for collisions
    for enemy in enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # Check for bullet collisions with enemies
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # Draw enemy explosions
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # Draw bullets
    player.bullets.draw(screen)

    # Draw enemies
    enemies1.draw(screen)

    # Draw score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # Update the screen
    pygame.display.update()

    # Process game exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Game over screen
screen.blit(game_over, (0, 0))
font = pygame.font.Font(None, 48)
text = font.render('Score: ' + str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(text, text_rect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()