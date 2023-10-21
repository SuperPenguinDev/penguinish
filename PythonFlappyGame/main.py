import pygame
import random

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Penguinish')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# miles to do: 4

# font
font = pygame.font.SysFont('Arial', 60)
black = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
started = False
gameOver = False
pipe_gap = 500
scroll_speed = 4
align_space_x = 65
align_space_y = 35
score = 0
pass_pipe = False
item_spawned = False
item_y_offset = 150

pipe_frequency = 2250
last_pipe = pygame.time.get_ticks() - pipe_frequency

images = ["Fish.png", "IceCube.png", "Music.png", "Basketball.png"]

new_img_index = -1
current_index = -1
update_item_img = True

def reset_game():
    global new_img_index
    global current_index
    global update_item_img
    draw_text(str(0), font, black, int(SCREEN_WIDTH / 2), 50)
    score = 0
    spike_group.empty()
    correct_group.empty()
    wrong_group.empty()
    player.rect.x = 100
    player.rect.y = 235
    player.image = pygame.transform.rotate(player.rotated, 0)
    # print(player.rect.y)
    new_img_index = -1
    current_index = -1
    update_item_img = True
    player.vel = 0
    return score
def blit_wanted_item(x, y):
    if current_index != -1:
        img = pygame.image.load(images[current_index])
        screen.blit(img, (x - 30, y))

def set_spawn_status(bool):
    item_spawned = bool

def spawn_items(rnd_height):

    correct_choice = random.randint(0, 3)

    global new_img_index
    new_img_index = correct_choice

    pos = random.randint(0, 1)

    possible_items = [0, 1, 2, 3]
    possible_items.remove(correct_choice)

    rnd = random.choice(possible_items)

    xpos = spike_group.sprites()[-1].rect.x

    if pos == 0:
        correct = CorrectItem(xpos, int(SCREEN_HEIGHT/2) - item_y_offset + rnd_height, correct_choice)
        correct_group.add(correct)
        wrong = WrongItem(xpos, int(SCREEN_HEIGHT/2) + item_y_offset + rnd_height, rnd)
        wrong_group.add(wrong)
    else:
        correct = CorrectItem(xpos, int(SCREEN_HEIGHT/2) + item_y_offset + rnd_height, correct_choice)
        correct_group.add(correct)
        wrong = WrongItem(xpos, int(SCREEN_HEIGHT/2) - item_y_offset + rnd_height, rnd)
        wrong_group.add(wrong)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    text_rect = img.get_rect(center = (SCREEN_WIDTH / 2, y))
    screen.blit(img, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('SidewaysPenguin.png')
        self.rotated = self.image
        self.rect = self.rotated.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.pressed = False
    
    def update(self):

        # Gravity
        if started == True:

            self.rect.y += int(self.vel)
            self.vel += 0.2
            if self.vel > 7:
                self.vel = 7
            if self.rect.bottom >= 590:
                self.rect.bottom = 590

            self.image = pygame.transform.rotate(self.rotated, self.vel)

        keys = pygame.key.get_pressed()

        if gameOver == False and started == True:

            # Jump
            if keys[pygame.K_SPACE] == 1 and self.pressed == False:
                self.vel = -6
                self.pressed = True

            if keys[pygame.K_SPACE] == 0 and self.pressed == True:
                self.pressed = False

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos

        if pos != 0:
            self.image = pygame.image.load('Spike2.png')
        else:
            self.image = pygame.image.load('MiddleSection.png')

        self.rect = self.image.get_rect()

        # pos 1 is top, pos -1 is btm, pos 0 is mid
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if pos == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        if pos == 0:
            self.rect.topleft = [x, y]
        
    def update(self):

        if self.rect.x >= -200:
            self.rect.x -= scroll_speed
        else:
            self.kill()

class CorrectItem(pygame.sprite.Sprite):
    def __init__(self, x, y, choice):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Fish.png')

        if choice == 0:
            self.image = pygame.image.load('Fish.png')
        elif choice == 1:
            self.image = pygame.image.load('IceCube.png')
        elif choice == 2:
            self.image = pygame.image.load('Music.png')
        else:
            self.image = pygame.image.load('Basketball.png')

        self.rect = self.image.get_rect()

        self.rect.center = [x + 85, y]
        
    def update(self):

        if self.rect.x >= -200:
            self.rect.x -= scroll_speed
        else:
            self.kill()

class WrongItem(pygame.sprite.Sprite):
    def __init__(self, x, y, choice):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Fish.png')

        if choice == 0:
            self.image = pygame.image.load('Fish.png')
        elif choice == 1:
            self.image = pygame.image.load('IceCube.png')
        elif choice == 2:
            self.image = pygame.image.load('Music.png')
        else:
            self.image = pygame.image.load('Basketball.png')

        self.rect = self.image.get_rect()

        self.rect.center = [x + 85, y]
        
    def update(self):

        if self.rect.x >= -200:
            self.rect.x -= scroll_speed
        else:
            self.kill()

player_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
correct_group = pygame.sprite.Group()
wrong_group = pygame.sprite.Group()

player = Player(100, int(SCREEN_HEIGHT / 2))

player_group.add(player)

# btm_spike = Spike(800, int(SCREEN_HEIGHT / 2), -1)
# mid_spike = Spike(800 + align_space_x, int(SCREEN_HEIGHT / 2) - align_space_y, 0)
# top_spike = Spike(800, int(SCREEN_HEIGHT / 2), 1)
# spike_group.add(btm_spike)
# spike_group.add(mid_spike)
# spike_group.add(top_spike)

run = True
while run:

    clock.tick(60)

    screen.fill((255,255,255))

    player_group.draw(screen)
    player_group.update()
    spike_group.draw(screen)
    correct_group.draw(screen)
    wrong_group.draw(screen)

    if started == False:
        draw_text(str("Click to Start"), font, black, int(SCREEN_WIDTH / 2), 50)

    if gameOver == False and started == True:
        blit_wanted_item(int(SCREEN_WIDTH/2), 100)

        if update_item_img == True:
            current_index = new_img_index
            if current_index != -1:
                update_item_img = False

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            rnd_height = random.randint(-35, 35)
            btm_spike = Spike(800, int(SCREEN_HEIGHT / 2) + rnd_height, -1)
            mid_spike = Spike(800 + align_space_x, int(SCREEN_HEIGHT / 2) - align_space_y + rnd_height, 0)
            top_spike = Spike(800, int(SCREEN_HEIGHT / 2) + rnd_height, 1)
            spike_group.add(btm_spike)
            spike_group.add(mid_spike)
            spike_group.add(top_spike)
            spawn_items(rnd_height)
            set_spawn_status(False)
            last_pipe = time_now

        spike_group.update()
        correct_group.update()
        wrong_group.update()
        if pygame.sprite.groupcollide(player_group, correct_group, False, True):
            score += 1
            update_item_img = True
        if pygame.sprite.groupcollide(player_group, wrong_group, False, True):
            if score > 0:
                score -= 1
            update_item_img = True

        draw_text(str(score), font, black, int(SCREEN_WIDTH / 2), 50)
    
    if pygame.sprite.groupcollide(player_group, spike_group, False, False) or player.rect.top < 0:
        gameOver = True
        draw_text(str("Click to Restart"), font, black, int(SCREEN_WIDTH / 2), 50)

    # if len(spike_group) > 0:
    #     if player_group.sprites()[0].rect.left > spike_group.sprites()[0].rect.left\
    #         and player_group.sprites()[0].rect.right < spike_group.sprites()[0].rect.right\
    #         and pass_pipe == False:
    #         pass_pipe = True
    #     if pass_pipe == True:
    #         if player_group.sprites()[0].rect.left > spike_group.sprites()[0].rect.right:
    #             score += 1
    #             pass_pipe = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and started == False and gameOver == False:
            started = True
        if gameOver == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                score = reset_game()
                gameOver = False
                started = False
     
    pygame.display.update()
    
pygame.quit()