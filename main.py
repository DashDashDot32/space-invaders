import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
player_dx = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_dx = []
enemy_dy = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(10)
    enemy_dx.append(5)
    enemy_dy.append(40)

# Bullet 
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_dy = 10
bullet_state = "ready" # Ready - you can't see the bullet on the screen, Fire - The bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

# Game Loop        
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -7 # Move to the left if the left arrow is down
            if event.key == pygame.K_RIGHT:
                player_dx = 7 # Move to the right if the right arrow is down
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0 # Reset speed to 0 when the key is released

    # Background Color - RGB    
    screen.fill((0,204,204))
    screen.blit(background, (0,0))

    # Set Player Speed
    playerX += player_dx
    
    # Set movement borders for the player
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    
    
    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemy_dx[i]    
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemy_dx[i] *= -1
            enemyY[i] += enemy_dy[i]
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemy_dx[i] *= -1
            enemyY[i] += enemy_dy[i]
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 100
            enemyX[i] = random.randint(0,736)
            enemyY[i] = 10

        enemy(enemyX[i],enemyY[i], i)

    # Bullet Movement
    if bulletY <= -32:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bullet_dy

    player(playerX,playerY)
    show_score(textX,textY)

    # Will always be here, need this to update the display every iteration of the loop
    pygame.display.update()
    