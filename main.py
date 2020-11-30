import pygame

import math

import random

from pygame import mixer

pygame.init()

S_Width = 800
S_Height = 600
screen = pygame.display.set_mode((S_Width, S_Height))

# title
pygame.display.set_caption("SPACE Invaders")

icon = pygame.image.load('spaceship.png')

pygame.display.set_icon(icon)

# Screen
Screen_BackGround = (0, 0, 0)

background = pygame.image.load('Back.png')

# Player
player_img = pygame.image.load('space-invaders.png')

X_Player = 100.0

Y_Player = 480.0

Play_Change = 0.0

# Enemy
Enemy_number = 20

enemy_img = []

enemy_X = []

enemy_Y = []

Enemy_X_Change = []

Enemy_Y_Change = []
for i in range(Enemy_number):
    enemy_img.append(pygame.image.load('enemy.png'))

    enemy_X.append(random.randint(0, 735))

    enemy_Y.append(random.randint(50, 300))

    Enemy_X_Change.append(1)

    Enemy_Y_Change.append(100)

# Bullet
bullet_img = pygame.image.load('bullet.png')

bullet_X = 0.0

bullet_Y = 480.0

bullet_X_Change = 0.0

bullet_Y_Change = 10.0

bullet_Status = "ready"

player_status = 1

# Printing score font
text_x = 10
text_y = 10
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
# game over mode
over_font = pygame.font.Font('freesansbold.ttf', 64)
win_font = pygame.font.Font('freesansbold.ttf', 64)


def winner_game_over():
    c_sound = mixer.Sound('pie.wav')
    c_sound.play()
    win_text = win_font.render("Congratulation", True, (255, 255, 255))
    screen.blit(win_text, (200, 250))


def show_game_over():
    s_sound=mixer.Sound('na.wav')
    s_sound.play()
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score():
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (text_x, text_y))


def player(x=100.0, y=480.0):
    screen.blit(player_img, (x, y))


def enemy(x, y, j):
    screen.blit(enemy_img[j], (x, y))


def bullet(x=X_Player, y=480):
    global bullet_Status
    bullet_Status = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


# calc collision


def is_collision(x_enemy, y_enemy, x_bullet, y_bullet):
    distance = math.sqrt((math.pow(x_enemy - x_bullet, 2)) + (math.pow(y_enemy - y_bullet, 2)))
    if distance < 25:
        return True
    else:
        return False


running = True
# main program

while running:
    screen.fill(Screen_BackGround)
    screen.blit(background, (0, 0))
    # Checking User Entry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # detect motion of space ship
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Play_Change = -5
            elif event.key == pygame.K_RIGHT:
                Play_Change = 5

            # detect weapon button
            elif event.key == pygame.K_SPACE:
                if bullet_Status is "ready":
                    # command of bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    bullet_X = X_Player

                    bullet(bullet_X, bullet_Y)

            # elif event.key == pygame.K_SPACE :
        # insert continue option
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                Play_Change = 0.0

    # Update Player input data

    X_Player += Play_Change
    if X_Player <= 0:
        X_Player = 0
    elif X_Player >= 736:
        X_Player = 736

    # Update Enemy movement
    for i in range(Enemy_number):

        if enemy_Y[i] > 550:
            for j in range(Enemy_number):
                enemy_Y[j] = 2000
            show_game_over()
            # running = False
            break

        enemy_X[i] += Enemy_X_Change[i]
        if enemy_X[i] <= 0:
            Enemy_X_Change[i] = 2
            enemy_Y[i] += Enemy_Y_Change[i]

        if enemy_X[i] >= 736:
            Enemy_X_Change[i] = -2
            enemy_Y[i] += Enemy_Y_Change[i]

        collision = is_collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)

        if collision:
            bullet_Y = 480
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()

            Enemy_number -= 1

            bullet_Status = "ready"

            score_value += 1

            enemy_X[i] = random.randint(0, 735)

            enemy_Y[i] = random.randint(50, 300)

        if player_status % 2 == 0:
            Enemy_Y_Change += 100
            Enemy_X_Change += 100

        enemy(enemy_X[i], enemy_Y[i], i)

    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_Status = "ready"

    if bullet_Status is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_Change

    player(X_Player, Y_Player)

    show_score()
    if Enemy_number <= 0:
        # implent func congratulation

        winner_game_over()

    pygame.display.update()
