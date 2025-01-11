import pygame
from pygame import sprite

class Cursor(sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()

        self.image = pygame.image.load(
            "resources/images/cursor/Cursor.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
