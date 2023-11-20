import pygame
from settings import *


class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.right_image = pygame.image.load("assets/images/blueplanet.png").convert()
        self.right_image.set_colorkey((0, 0, 0))
        self.image = self.right_image
        # creating a rectangle that tells where to paint shuttle
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))