import pygame
from pygame import sprite
from animate import Animation
from enum import Enum
from signaling import Signal

class ZombieState(Enum):
    MOVE = 0
    ATTACK = 1
    DIE = 2


def load_move_images():
    return [
        pygame.image.load(
            "resources/images/zombie/Zombie_{}.png".format(i)
        ).convert_alpha()
        for i in range(0, 22)
    ]


def load_die_images():
    die_images = [
        pygame.image.load(
            "resources/images/zombie/ZombieDie_{}.png".format(i)
        ).convert_alpha()
        for i in range(0, 10)
    ]
    # add fading effect to die images
    last_die_image = die_images[-1]
    for i in range(20):
        img = last_die_image.copy()
        img.set_alpha(255 - i * 255 // 20)
        die_images.append(img)
    return die_images


def load_attack_images():
    return [
        pygame.image.load(
            "resources/images/zombie/ZombieAttack_{}.png".format(i)
        ).convert_alpha()
        for i in range(0, 21)
    ]

def pow_animation():
    image = pygame.image.load("resources/images/fx/pow.png").convert_alpha()
    w, h = image.get_size()
    ratio = [0.5, 0.75] + [1.0 for _ in range(20)] + [0.75, 0.5, 0.25]
    return [
        pygame.transform.scale(image, (int(w * r), int(h * r)))
        for r in ratio
    ]


class Zombie(sprite.Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super(Zombie, self).__init__()

        self.move_animation = Animation(load_move_images(), repeat=True)
        self.attack_animation = Animation(load_attack_images(), repeat=True)
        self.die_animation = Animation(load_die_images(), repeat=False)

        self.image = self.move_animation.get_first_frame()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 100
        self.dps = 1 # 1 damage per second
        self.is_alive = True
        self.kill_signal = Signal()

        self.pow_animation = Animation(pow_animation(), repeat=False)
        self.pos_hit = None

    def update(self, dt: float, targets: sprite.Group, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.is_alive = False
                    if self.pos_hit is None:
                        self.pos_hit = event.pos
                        self.kill_signal.emit() # emit to game manager that this zombie is dead and run only once

        target = self.look_for_closest_target(targets)
        if target is None:
            return

        orientation = self.determine_orientation(target)
        if self.is_alive:
            colliding = self.rect.colliderect(target.rect)

            if colliding: # attack
                self.image = self.attack_animation.next_frame(flip=orientation)
                dmg = self.dps * dt
                target.receive_dmg(dmg)
            else:
                self.image = self.move_animation.next_frame(flip=orientation)

                # move towards target
                direction = pygame.Vector2(target.rect.center) - self.rect.center
                direction.normalize_ip()
                self.rect.move_ip(direction * self.speed * dt)
        else:
            self.image = self.die_animation.next_frame(flip=orientation)
            if self.image is None:
                self.kill()

    def look_for_closest_target(self, targets: sprite.Group):
        if len(targets) == 0:
            return None

        pos = pygame.Vector2(self.rect.center)
        closest_target = min(targets, key=lambda x: pos.distance_to(x.rect.center))
        return closest_target

    def determine_orientation(self, target) -> bool:
        return target.rect.centerx >= self.rect.centerx

    def draw_pow_fx(self, screen):
        if not self.is_alive and not self.pow_animation.is_ended():
            img = self.pow_animation.next_frame()
            assert img is not None
            rect = img.get_rect(center=self.pos_hit)
            screen.blit(img, rect)
