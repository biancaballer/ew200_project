import pygame
import sys
import random
import shuttle
import planet
import laser
from meteor import Meteor, meteors
from settings import *

pygame.init()

running = True
game_font = pygame.font.Font(None, 50)  # none works but make a unique font

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Blast")
# make space stuff
star = pygame.image.load("assets/images/star1.png").convert()
star.set_colorkey((0, 0, 0))
score = 0
my_shuttle = shuttle.Shuttle(20, 380)  # create a new shuttle
my_planet = planet.Planet(500, 30)
scaled_planet = pygame.transform.scale(my_planet.image, (int(my_planet.rect.width * SCALE_FACTOR),
                                                         int(my_planet.rect.height * SCALE_FACTOR)))  # scales planet
my_planet.image = scaled_planet

#  make while running instead of for loop - 
while running:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
        elif event.type == pygame.ACTIVEEVENT:
            meteors.add(Meteor(random.randint(0, SCREEN_WIDTH - TILE_SIZE),
                               random.randint(0, SPACE_BOTTOM - TILE_SIZE)))
# make continuous projection of meteors until planet gets hit 3 times
background = screen.copy()
clock = pygame.time.Clock()


def draw_background():
    # draw space
    background.fill(SPACE_COLOR)
    # randomly place stars
    for _ in range(25):
        x = random.randint(0, SCREEN_WIDTH)
        # offset the stars so it looks better :)
        y = random.randint(0, SCREEN_HEIGHT) - (0.5 * TILE_SIZE)  # stars go all over screen
        background.blit(star, (x, y))
    # draw the meteor blast title
    text = game_font.render("Meteor Blast", True, (216, 242, 242))

    background.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))


draw_background()

while len(meteors) > 0:
    # listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                my_shuttle.moving_left = True
            if event.key == pygame.K_RIGHT:
                my_shuttle.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                my_shuttle.moving_left = False
            if event.key == pygame.K_RIGHT:
                my_shuttle.moving_right = False

    # update game objects
    my_shuttle.update()
    meteors.update()

    # check for collisions
    blasted_meteors = pygame.sprite.spritecollide(my_shuttle, meteors, True)  # change score fxn
    score += len(blasted_meteors)
    if len(blasted_meteors) > 0:
        print(f"You blasted a meteor, your score is {score}!")
    # draw the game screen
    screen.blit(background, (0, 0))
    my_shuttle.draw(screen)
    my_planet.draw(screen)

    # add planet collision update

    meteors.draw(screen)
    pygame.display.flip()
    clock.tick(60)
# projectiles - use trig for x and y speed
