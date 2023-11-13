import pygame
import sys
import random
from settings import *
pygame.init()

game_font = pygame.font.Font("assets/fonts/spaceage.ttf", 128)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Blast")
# projectiles - use trig for x and y speed