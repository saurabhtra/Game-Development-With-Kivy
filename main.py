import pygame
import random
import math
from pygame import mixer

# intialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("background.png")
#background music
mixer.music.load('music background.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("SUPER")
icon = pygame.image.load("pic.jpg")
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load('airplane.png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('kivy.png'))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# bullet
# Ready -you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

txtX = 10
txtY = 10
# Game over
over_font = pygame.font.Font('freesansbold.ttf', 100)



def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over_font(x,y):
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (100,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 25:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    enemyX: float
    enemyY: float
    # RGB color
    screen.fill((0, 0, 0))
 # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
# bullet with space bar
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound =mixer.Sound('bullet sound.mp3')
                    bullet_Sound.play()
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
 # checking for boundaries of spaceship so ity doesn't go out of boounds
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 738:
        playerX = 738
 # movement of enemy
    for i in range(num_of_enemies):
     # game over
        if enemyY[i] >400:
            for j in range(num_of_enemies):
                enemyY[j] =2000
            game_over_font(200,200)
            break
        enemyX[i] += enemyX_change[i]
        #enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
             enemyY[i] += enemyY_change[i]
             enemyX_change[i] = -1
            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explotion_Sound = mixer.Sound('kill sound.wav')
            explotion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1


            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
# bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(txtX, txtY)
    pygame.display.update()
