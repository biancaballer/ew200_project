import pygame
from settings import *
import math


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the mouse position and the center of the shuttle
        angle = math.atan2(mouse_y, mouse_x)

        self.right_image = pygame.image.load("assets/images/laser.png").convert()
        self.rect = self.right_image.get_rect()
        self.right_image.set_colorkey((0, 0, 0))
        self.image = self.right_image
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.angle = math.radians(90)  # Set the angle to 90 degrees

    def update(self):
        laser_speed = 5
        self.rect.y -= laser_speed * math.sin(self.angle)
        # self.rect.y -= 5
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


lasers = pygame.sprite.Group()
