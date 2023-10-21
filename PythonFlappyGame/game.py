import pygame
import random

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Penguinish')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# loading player image
playerImg = pygame.image.load("SidewaysPenguin.png")
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_y_change = 0

global pressed 
pressed = False

def drawPlayer(x, y):
    global player_y_change
    global playerImg
    rotatedImg = pygame.transform.rotate(playerImg, player_y_change)
    screen.blit(rotatedImg, (x, y))

def apply_gravity():
    global player_y_change
    player_y_change += 0.2

# Spikes
bSpike = pygame.image.load("Spike.png")
tSpike = pygame.transform.flip(bSpike, False, True)
mSpike = pygame.image.load("MiddleSpike.png")
gap_size = 175
spikes_x = 800
spike_x_motion = -3
random_y = random.randint(-250, -150)

def draw_spikes():
    bSpikeY = SCREEN_HEIGHT - abs(random_y) + gap_size
    screen.blit(bSpike, (spikes_x, bSpikeY))
    screen.blit(tSpike, (spikes_x, random_y))
    screen.blit(mSpike, (spikes_x + 75, (bSpikeY + random_y)/2 + 125))

def check_collision(player_x, player_y, spikes_x, random_y):
    if player_x >= spikes_x - 50 and player_x <= spikes_x + 50:
        if player_y >= 450 or player_y <= 100:
            return True
    return False

run = True

while run:

    clock.tick(60)

    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and pressed == False:
                player_y_change = -5
                pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pressed = False

    screen.fill((255,255,255))

    spikes_x += spike_x_motion
    if spikes_x <= -200:
        spikes_x = 800
        random_y = random.randint(-250, -150)
        spike_x_motion = -3

    draw_spikes()

    apply_gravity()

    if player_y_change >= 7:
        player_y_change = 7

    player_y += player_y_change

    if player_y <= 0:
        player_y /= 2
        player_y_change += 0.2
    if player_y >= 450:
        player_y = 450
        spike_x_motion = -5

    drawPlayer(player_x, player_y)

    collision = check_collision(player_x, player_y, spikes_x, random_y)
    if collision:
        print("Game Over")  # You can replace this with your game over logic

    pygame.display.flip()

pygame.quit()