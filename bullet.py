import pygame
import numpy as np

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, screen_size):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(
            "resources/images/bullet/Bullet_1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.margin = 50  # if bullet is out of screen by this margin, remove it
        self.speed = 200
        self.direction = self.get_random_direction(screen_size)
        self.screen_size = screen_size

    def get_random_direction(self, screen_size):
        screen_w, screen_h = screen_size
        vec_tl = pygame.Vector2(0, 0) - self.rect.center
        vec_tr = pygame.Vector2(screen_w, 0) - self.rect.center
        vec_bl = pygame.Vector2(0, screen_h) - self.rect.center
        vec_br = pygame.Vector2(screen_w, screen_h) - self.rect.center

        # get two vectors which their angles cover the screen
        # knowing that bullet initial position is out of the screen
        pairs = [
            (i.normalize(), j.normalize())
            for i in (vec_tl, vec_tr, vec_bl, vec_br)
            for j in (vec_tl, vec_tr, vec_bl, vec_br)
            if i != j
        ]
        largest_angle_pair = max(pairs, key=lambda pair: pair[0].angle_to(pair[1]))
        # random direction between the two vectors
        v1, v2 = largest_angle_pair
        # random between 0 and 1 with normal distribution
        r = np.random.beta(5, 5)
        v = v1.lerp(v2, r) # v1 + r * (v2 - v1)
        return v.normalize()

    def is_out_of_screen(self):
        screen_w, screen_h = self.screen_size
        x, y = self.rect.center
        return x < -self.margin or x > screen_w + self.margin or y < -self.margin or y > screen_h + self.margin

    def update(self, dt) -> None:
        self.rect.move_ip(self.direction * self.speed * dt)
        if self.is_out_of_screen():
            self.kill()

    def collide_with_cursor(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
