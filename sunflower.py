import pygame
from animate import Animation

RED = (255, 0, 0)
GREEN = (0, 255, 0)
SUNFLOWER_HEALTH = 5.0

class Sunflower(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super(Sunflower, self).__init__()
        self.animation = Animation(
            [
                pygame.image.load(
                    "resources/images/sunflower/SunFlower_{:02d}.png".format(i)
                ).convert_alpha()
                for i in range(0, 13)
            ],
            repeat=True,
        )

        self.image = self.animation.get_first_frame()
        self.rect = self.image.get_rect(center=pos)
        self.health = SUNFLOWER_HEALTH

    def receive_dmg(self, dmg: float):
        self.health = max(0, self.health - dmg)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.centerx - 50, self.rect.bottom + 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - 50, self.rect.bottom + 10, int(100 * (self.health / SUNFLOWER_HEALTH)), 10)) 

    def update(self) -> None:
        if self.health <= 0:
            return self.kill()

        self.image = self.animation.next_frame()
