import pygame
import sys
import random
import shuttle
import planet
from laser import *
from meteor import Meteor, meteors
from settings import *

pygame.init()

running = True  # flag
high_score = 0
score = 0
game_font = pygame.font.Font("assets/fonts/spaceage.ttf", 22)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Blast")
# make space stuff
star = pygame.image.load("assets/images/star1.png").convert()
star.set_colorkey((0, 0, 0))
my_shuttle = shuttle.Shuttle(20, 380)  # create a new shuttle
shuttle_rect = pygame.Rect(50, 50, 50, 50)
shuttle_vel = [5, 2]  # Initial velocity as a vector [vel_x, vel_y]
my_planet = planet.Planet(500, 30)
scaled_planet = pygame.transform.scale(my_planet.image, (int(my_planet.rect.width * SCALE_FACTOR),
                                                         int(my_planet.rect.height * SCALE_FACTOR)))  # scales planet
my_planet.image = scaled_planet
pygame.mixer.music.load("assets/sounds/space_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # plays background music in infinite loop
blaster_sound = pygame.mixer.Sound("assets/sounds/laserblast.mp3")
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    # If the file doesn't exist, set a default high score
    high_score = 0
for _ in range(NUM_METEORS):
    meteors.add(Meteor(random.randint(0, 10),
                       random.randint(0, 0)))

# make continuous projection of meteors until planet gets hit 3 times
background = screen.copy()
clock = pygame.time.Clock()


# background function
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
    global score, high_score
    # Update the high score if the current score is higher
    if score > high_score:
        high_score = score
        # Save the new high score to the file
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
    screen.fill(SPACE_COLOR)
    text = game_font.render(f"Game Over - Your Score: {score} - High Score: {high_score}", True, 0)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting_for_key = True  # flag
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.event.clear()

    return False


# main game screen
def main_game():
    global score  # used global variables to be able to access in and out of function
    game_over = False  # credit Arya
    music_paused = False  # flag for background music
    hits = 0
    draw_background()
    while not game_over:
        # listen for events
        # continuously adds a new meteor periodically
        # Update shuttle position based on velocity
        shuttle_rect.x += shuttle_vel[0]
        shuttle_rect.y += shuttle_vel[1]

        # elastic collision between shuttle and wall by reversing velocity
        if shuttle_rect.left < 0 or shuttle_rect.right > SCREEN_WIDTH:
            shuttle_vel[0] *= -1  # Reverse horizontal velocity on wall collision

        if shuttle_rect.top < 0 or shuttle_rect.bottom > SCREEN_HEIGHT:
            shuttle_vel[1] *= -1  # Reverse vertical velocity on wall collision
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
                        music_paused = False
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
        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (150, 150))
        # shows score during game
        hit_planet = pygame.sprite.spritecollide(my_planet, meteors, False)
        if hit_planet:
            hits += 1
            # my_planet.hit()  # changes planet image to show damage
        while hits >= 3:
            hits = 0
            game_done = end_screen()
            if game_done:
                hits = 0
                my_planet.reset()
                scale_planet = pygame.transform.scale(my_planet.image, (int(my_planet.rect.width * SCALE_FACTOR),
                                                                        int(my_planet.rect.height * SCALE_FACTOR)))  # scales planet
                my_planet.image = scale_planet
                main_game()
                # break

                # continue

        meteors.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# main game loop
while running:
    running = False
    main_game()
