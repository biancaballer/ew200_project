import pygame
import sys
import random
import shuttle
from meteor import Meteor, meteors
from settings import *

pygame.init()

game_font = pygame.font.Font("assets/fonts/spaceage.ttf", 128)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Blast")
# make space stuff
sand_top = pygame.image.load("assets/images/sand_top.png").convert()
seagrass = pygame.image.load("assets/images/seagrass.png").convert()
seagrass.set_colorkey((0, 0, 0))
sand_top.set_colorkey((0, 0, 0))
score = 0
my_fish = fish.Fish(200, 200)  # create a new fish

for _ in range(NUM_MINNOWS):
    minnows.add(Minnow(random.randint(0, SCREEN_WIDTH - TILE_SIZE),
                       random.randint(0, SPACE_BOTTOM - TILE_SIZE)))

background = screen.copy()
clock = pygame.time.Clock()


def draw_background():
    # draw space
    background.fill(SPACE_COLOR)
    # sandy bottom
    for i in range(SCREEN_WIDTH // TILE_SIZE):
        background.blit(sand, (TILE_SIZE * i, SCREEN_HEIGHT - TILE_SIZE))
        background.blit(sand_top, (TILE_SIZE * i, SCREEN_HEIGHT - (2 * TILE_SIZE)))
    # randomly place stars
    for _ in range(4):
        x = random.randint(0, SCREEN_WIDTH)
        # offset the seaweed so it looks better :)
        y = random.randint(SCREEN_HEIGHT - 2 * TILE_SIZE, SCREEN_HEIGHT) - (0.5 * TILE_SIZE)
        background.blit(seagrass, (x, y))
    # draw the CHOMP! title
    text = game_font.render("Meteor Blast", True, (216, 242, 242))

    background.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))


draw_background()

while len(minnows)>0:
    # listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                my_fish.moving_left = True
            if event.key == pygame.K_RIGHT:
                my_fish.moving_right = True
            if event.key == pygame.K_UP:
                my_fish.moving_up = True
            if event.key == pygame.K_DOWN:
                my_fish.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                my_fish.moving_left = False
            if event.key == pygame.K_RIGHT:
                my_fish.moving_right = False
            if event.key == pygame.K_UP:
                my_fish.moving_up = False
            if event.key == pygame.K_DOWN:
                my_fish.moving_down = False
        # elif event.type == pygame.MOUSEMOTION:
            # my_minnow.rect.center = pygame.mouse.get_pos()


    # update game objects
    my_fish.update()
    minnows.update()

    # check for collisions
    chomped_minnows = pygame.sprite.spritecollide(my_fish, minnows, True)
    score += len(chomped_minnows)
    if len(chomped_minnows) >0:
        print(f"Chomped a minnow, your score is {score}!")
    # draw the game screen
    screen.blit(background, (0, 0))
    my_fish.draw(screen)

    minnows.draw(screen)
    pygame.display.flip()
    clock.tick(60)
# projectiles - use trig for x and y speed