# A game of space invaders
# use of py game module

import pygame
import random
import math
from pygame import mixer  # when we have to do anything with sound s

# initialize the py game
pygame.init()

# create a screen
# adding another bracket is necessary
screen = pygame.display.set_mode((800, 600))
# 800  is width and 600 is height

# Background
background = pygame.image.load('2799006.jpg')

# Background Sound
mixer.music.load('bgsound.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Martian")
# choose the 32px image
# to upload the icon image to pycharm
# just drag the image folder to the project folder(Martian here)in the side box or file viewer.
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('shootingrocket.png')
playerX = 370  # less than half of width
playerY = 480  # less than height
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

'''enemyImg = pygame.image.load('enemy.png')
# enemyX = 370  # less than half of width
# enemyY = 50
# enemyX = random.randint(0, 800)
enemyX = random.randint(0, 735)  # 736 to 735
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 40'''

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # less than half of width
bulletY = 480  # less than height
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score = 0

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)  # .ttf extension of the font

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 40)


def game_intro():
    intro = True
    while intro:
        pygame.display.fill(0, 255, 255)
        print("Welcome to MARTIAN \n The objective of the game is to destroy UFO's\n"
              "Don't let the UFO'S come near you otherwise you will die!")
        pygame.display.update()
        pygame.time.Clock()


def show_score(x, y):
    score = font.render('SCORE: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render('GAME OVER  SCORE: ' + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (150, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    # make bullet_state as global so that it can be accessed inside this function
    global bullet_state
    bullet_state = "fire"
    # to draw bullet on screen
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:  # by trial
        return True
    else:
        return False


# game loop so that window works
# anything that you want to be persistent inside a game window
# and you want it to appear on display either an image or text that it has to be inside infinite loop


running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 255, 255))  # two brackets max color = 255
    # Background image
    screen.blit(background, (0, 0))
    # playerY -= 0.2
    # event is any kind of input control for example we close the window by clicking button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # remember quit syntax here
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:  # key down is pressing of the key
            # print("Keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                # print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                # print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Gun.wav')
                    bullet_sound.play()
                    # get the current x cord of spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                # print("Keystroke has been released")

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking boundaries of spaceship so it does not go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # subtract 64 from 800
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(350, 300)
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # subtract 64 from 800
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('ufodead.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    '''enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:  # subtract 64 from 800
        enemyX_change = -4
        enemyY += enemyY_change'''

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change

    # Collision
    '''collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)'''

    player(playerX, playerY)  # after screen as the screen is drawn first
    # enemy(enemyX, enemyY)
    show_score(610, 20)
    pygame.display.update()  # this is always going to be present in py game
