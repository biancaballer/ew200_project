import pygame
from settings import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = None
        self.right_image = pygame.image.load("assets/images/laser.png").convert()
        self.right_image.set_colorkey((0, 0, 0))
        self.image = self.right_image
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())

    def update(self):
        self.rect.y -= 5
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


lasers = pygame.sprite.Group()