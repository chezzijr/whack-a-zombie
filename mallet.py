import pygame
from pygame import sprite
from animate import Animation

RED = (255, 0, 0)
GREEN = (0, 255, 0)
HEALTH = 10

def rotate(angle):
    return lambda image: pygame.transform.rotate(image, angle)

# use a mallet as cursor
class Mallet(sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        sequence_of_rotations = [rotate(angle) for angle in range(30, 130, 25)] + \
                                [rotate(angle) for angle in range(130, 30, -25)]

        self.animation = Animation([
            rotation(
                pygame.image.load("resources/images/mallet/mallet.png").convert_alpha()
            )
            for rotation in sequence_of_rotations
        ], repeat=False)
        self.image = self.animation.get_first_frame()
        self.rect = self.image.get_rect()

        pygame.mouse.set_visible(False)
        self.whacking = False
        self.health = 10

    def update(self):
        cursor_pos = pygame.mouse.get_pos()
        self.rect.center = cursor_pos
        if any(pygame.mouse.get_pressed()):
            self.whacking = True
            self.animation.reset()

        if self.whacking:
            image = self.animation.next_frame()
            if image is not None:
                self.image = image
            else:
                self.image = self.animation.get_first_frame()
                self.whacking = False

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.centerx - 25, self.rect.bottom + 5, 50, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - 25, self.rect.bottom + 5, int(50 * (self.health / HEALTH)), 5)) 

    def receive_dmg(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.kill()
