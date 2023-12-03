import pygame
from settings import *
import laser


class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.planet_0 = pygame.image.load("assets/images/blueplanet.png").convert()
        self.planet_0.set_colorkey((0, 0, 0))
        self.planet_1 = pygame.image.load("assets/images/planet1.png").convert()
        self.planet_1.set_colorkey((0, 0, 0))
        self.image = self.planet_0
        # creating a rectangle that tells where to paint shuttle
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    #  make collision where planet updates after hits and game ends after 3 hits
    def hit(self):
        self.image = self.planet_1

    def reset(self):
        self.image = self.planet_0
