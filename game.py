import pygame
import sys
import random
import shuttle
import planet
from laser import *
from meteor import Meteor, meteors
from settings import *

pygame.init()

# running = True
game_font = pygame.font.Font(None, 50)  # none works but make a unique font

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Blast")
# make space stuff
star = pygame.image.load("assets/images/star1.png").convert()
star.set_colorkey((0, 0, 0))
my_shuttle = shuttle.Shuttle(20, 380)  # create a new shuttle
my_planet = planet.Planet(500, 30)
scaled_planet = pygame.transform.scale(my_planet.image, (int(my_planet.rect.width * SCALE_FACTOR),
                                                         int(my_planet.rect.height * SCALE_FACTOR)))  # scales planet
my_planet.image = scaled_planet
pygame.mixer.music.load("assets/sounds/space_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # plays background music in infinite loop
blaster_sound = pygame.mixer.Sound("assets/sounds/laserblast.mp3")
for _ in range(NUM_METEORS):
    meteors.add(Meteor(random.randint(0, 10),
                       random.randint(0, 0)))

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


# Function to display end screen
def end_screen():
    screen.fill(SPACE_COLOR)
    text = game_font.render("Game Over - Press R to Restart or Q to Quit", True, 0)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.event.clear()

    return False


# main game loop
def main_game():
    game_over = False  # credit Arya
    music_paused = False  # flag for background music
    score = 0
    hits = 0
    while not game_over:
        # listen for events
        # continuously adds a new meteor periodically
        if random.randint(1, 50) == 1:
            new_meteor = Meteor(80, 20)
            meteors.add(new_meteor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    my_shuttle.moving_left = True
                if event.key == pygame.K_RIGHT:
                    my_shuttle.moving_right = True
                if event.key == pygame.K_SPACE:
                    my_shuttle.shoot()
                    if not music_paused:
                        # Pause the background music
                        pygame.mixer.music.pause()
                        music_paused = True
                        # Play the additional sound effect
                        blaster_sound.play()
                    else:
                        # Unpause the background music
                        pygame.mixer.music.unpause()
                        music_paused = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    my_shuttle.moving_left = False
                if event.key == pygame.K_RIGHT:
                    my_shuttle.moving_right = False

        # update game objects
        my_shuttle.update()
        meteors.update()

        blasted_meteors = pygame.sprite.groupcollide(meteors, lasers, True, True)
        # checks for meteor v laser collision
        score += len(blasted_meteors)
        if len(blasted_meteors) > 0:
            print(f"You blasted a meteor, your score is {score}!")
        # draw the game screen
        screen.blit(background, (0, 0))
        my_shuttle.draw(screen)
        my_planet.draw(screen)
        lasers.draw(screen)
        lasers.update()

        hit_planet = pygame.sprite.spritecollide(my_planet, meteors, False)
        if hit_planet:
            hits += 1
            # my_planet.hit()  # changes planet image to show damage
        while hits >= 3:
            game_over = end_screen()
            if game_over:
                hits = 0
                score = 0

        meteors.draw(screen)
        pygame.display.flip()
        clock.tick(60)


draw_background()
main_game()
