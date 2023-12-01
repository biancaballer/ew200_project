import pygame
from settings import *
from laser import *


class Shuttle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.right_image = pygame.image.load("assets/images/blueshuttle.png").convert()
        self.right_image.set_colorkey((0, 0, 0))
        self.image = self.right_image
        # creating a rectangle that tells where to paint shuttle
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.lasers_group = lasers

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.moving_left:
            self.rect.x -= 5
            self.image = self.right_image
        elif self.moving_right:
            self.rect.x += 5
            self.image = self.right_image
        # make sure this puts the shuttle in a valid position
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SPACE_BOTTOM:  # accounts for space background
            self.rect.bottom = SPACE_BOTTOM

    def shoot(self):
        # Create a new laser and add it to the lasers group
        laser = Laser(self.rect.right, self.rect.centery)
        self.lasers_group.add(laser)
