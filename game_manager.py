import pygame
import random
import pygame_menu
import math
from sunflower import Sunflower
from pygame import sprite
from zombie import Zombie

WHITE = (255, 255, 255)

class GameManager:
    def __init__(self, width = 1280, height = 720):
        pygame.init()

        self.width = width
        self.height = height
        self.global_screen = pygame.display.set_mode((self.width, self.height))
        self.highscore = 0
        self.background = pygame.image.load("resources/images/background/bg.png")

    def game_round(self):
        screen_w, screen_h = self.global_screen.get_size()
        clock = pygame.time.Clock()

        sunflower_group = sprite.Group()
        zombie_group = sprite.Group()
        sunflower_group.add(Sunflower(pygame.Vector2(screen_w // 2, screen_h // 2)))

        zombie_spawn_interval = 3
        time_since_last_zombie_spawn = zombie_spawn_interval # spawn immediately
        
        bullet_spawn_interval = 1
        time_since_last_bullet_spawn = bullet_spawn_interval

        interval_for_next_level = 10
        interval_for_a_point = 1

        time_elapsed = 0
        score = 0
        level = 1

        while True:
            dt = clock.tick(24) / 1000 # in seconds
            time_since_last_zombie_spawn += dt
            time_since_last_bullet_spawn += dt

            time_elapsed += dt
            score = math.floor(time_elapsed / interval_for_a_point)
            level = math.floor(time_elapsed / interval_for_next_level) + 1

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return score

            # spawner to spawn in a zombie
            if time_since_last_zombie_spawn >= zombie_spawn_interval / level:
                time_since_last_zombie_spawn = 0
                spawn_pos = random.choice([
                    pygame.Vector2(-50, random.randint(0, screen_h)), # left
                    pygame.Vector2(screen_w + 50, random.randint(0, screen_h)), # right
                    pygame.Vector2(random.randint(0, screen_w), -50), # top
                    pygame.Vector2(random.randint(0, screen_w), screen_h + 50) # bottom
                ])
                zombie_group.add(Zombie(pos=spawn_pos))

            # spawner to spawn in a bullet
            if time_since_last_bullet_spawn >= bullet_spawn_interval:
                time_since_last_bullet_spawn = 0

            zombie_group.update(dt, sunflower_group, events)
            sunflower_group.update()

            if len(sunflower_group) == 0:
                break

            if self.background:
                self.global_screen.blit(self.background, (0, 0))
            else:
                self.global_screen.fill(WHITE)
            zombie_group.draw(self.global_screen)
            sunflower_group.draw(self.global_screen)
            for sunflower in sunflower_group:
                sunflower.draw_health_bar(self.global_screen)

            font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 36)
            margin = 10
            # draw level at top left
            text = font.render(f"Level: {level}", True, (255, 255, 255))
            self.global_screen.blit(text, (margin, margin)) # 10 pixels margin

            # draw score at top right
            text = font.render(f"Score: {score}", True, (255, 255, 255))
            self.global_screen.blit(text, (screen_w - text.get_width() - margin, margin))

            pygame.display.flip()
        return score

    def run(self):
        while True:
            score = self.game_round()
            
            # Game over screen
            menu = pygame_menu.Menu("Game Over", 300, 400, surface=self.global_screen)
            if score > self.highscore:
                self.highscore = score
                menu.add.label(f"New Highscore: {self.highscore}")
            else:
                menu.add.label(f"Score: {score}")
                menu.add.label(f"Highscore: {self.highscore}")
            menu.add.button("Play Again", action=lambda: menu.disable())
            menu.add.button("Quit", pygame_menu.events.EXIT)
            menu.mainloop(self.global_screen)


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
