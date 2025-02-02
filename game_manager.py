import pygame
import random
import pygame_menu
import math
from sunflower import Sunflower
from pygame import sprite
from zombie import Zombie
from bullet import Bullet
from mallet import Mallet

WHITE = (255, 255, 255)


class GameManager:
    def __init__(
        self,
        title="Whack-a-zombie",
        icon="resources/images/icon/icon.png",
        width=1280,
        height=720,
    ):
        pygame.init()

        self.width = width
        self.height = height

        self.global_screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        icon = pygame.image.load(icon)
        pygame.display.set_icon(icon)

        self.background = pygame.image.load("resources/images/background/bg.png")
        self.highscore = 0

    def game_round(self):
        pygame.mixer.init()
        screen_w, screen_h = self.global_screen.get_size()
        clock = pygame.time.Clock()

        sunflower_group = sprite.Group()
        zombie_group = sprite.Group()
        bullet_group = sprite.Group()
        cursor_group = sprite.GroupSingle()
        cursor_group.add(Mallet())

        bonk1_sound = pygame.mixer.Sound("resources/music/Bonk_1.mp3")
        bonk2_sound = pygame.mixer.Sound("resources/music/Bonk_2.mp3")

        splat_sound = pygame.mixer.Sound("resources/music/Splat.ogg")
        background_music = pygame.mixer.Sound("resources/music/background.mp3")
        eating_sound = pygame.mixer.Sound("resources/music/Zombie_Eating.mp3")

        num_sunflowers = 3
        for _ in range(num_sunflowers):
            x = random.randint(screen_w // 4, 3 * screen_w // 4)
            y = random.randint(screen_h // 4, 3 * screen_h // 4)
            sunflower_group.add(Sunflower(pygame.Vector2(x, y)))

        zombie_spawn_interval = 3
        time_since_last_zombie_spawn = zombie_spawn_interval  # spawn immediately

        bullet_spawn_interval = 1
        time_since_last_bullet_spawn = bullet_spawn_interval

        interval_for_next_level = 10

        time_elapsed = 0
        score = 0
        level = 1
        is_eating = False

        def on_zombie_die():
            nonlocal score
            score += 1
            random.choice([bonk1_sound, bonk2_sound]).play()

        background_music.play(-1, 0)

        def cleanup():
            background_music.stop()
            eating_sound.stop()

        while True:
            dt = clock.tick(30) / 1000  # in seconds
            time_since_last_zombie_spawn += dt
            time_since_last_bullet_spawn += dt

            time_elapsed += dt
            level = math.floor(time_elapsed / interval_for_next_level) + 1

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    cleanup()
                    pygame.quit()
                    return score

            # spawner to spawn in a zombie
            if time_since_last_zombie_spawn >= zombie_spawn_interval / level:
                time_since_last_zombie_spawn = 0
                spawn_pos = random.choice([
                    pygame.Vector2(-50, random.randint(0, screen_h)),  # left
                    pygame.Vector2(screen_w + 50, random.randint(0, screen_h)),  # right
                    pygame.Vector2(random.randint(0, screen_w), -50),  # top
                    pygame.Vector2(
                        random.randint(0, screen_w), screen_h + 50
                    ),  # bottom
                ])
                zombie = Zombie(pos=spawn_pos)
                zombie.kill_signal.connect(on_zombie_die)
                zombie_group.add(zombie)

            # spawner to spawn in a bullet
            if time_since_last_bullet_spawn >= bullet_spawn_interval / (level // 3 + 1):
                time_since_last_bullet_spawn = 0
                spawn_pos = random.choice([
                    pygame.Vector2(-40, random.randint(0, screen_h)),  # left
                    pygame.Vector2(screen_w + 40, random.randint(0, screen_h)),  # right
                    pygame.Vector2(random.randint(0, screen_w), -40),  # top
                    pygame.Vector2(
                        random.randint(0, screen_w), screen_h + 40
                    ),  # bottom
                ])
                bullet_group.add(
                    Bullet(pos=spawn_pos, screen_size=(screen_w, screen_h))
                )

            zombie_group.update(dt, sunflower_group, events)
            sunflower_group.update()
            bullet_group.update(dt)
            cursor_group.update()

            attacking = pygame.sprite.groupcollide(
                zombie_group, sunflower_group, False, False
            )
            # if there is collision
            if attacking and not is_eating:
                is_eating = True
                eating_sound.play(-1)
            elif not attacking and is_eating:
                is_eating = False
                eating_sound.stop()


            # check collision between bullet and cursor
            collisions = pygame.sprite.groupcollide(
                cursor_group, bullet_group, False, True
            )
            for cursor in collisions:
                cursor.receive_dmg(1)
                splat_sound.play()

            if self.background:
                self.global_screen.blit(self.background, (0, 0))
            else:
                self.global_screen.fill(WHITE)
            zombie_group.draw(self.global_screen)
            for zombie in zombie_group:
                zombie.draw_pow_fx(self.global_screen)

            sunflower_group.draw(self.global_screen)

            for sunflower in sunflower_group:
                sunflower.draw_health_bar(self.global_screen)

            bullet_group.draw(self.global_screen)
            cursor_group.draw(self.global_screen)

            for cursor in cursor_group:
                cursor.draw_health_bar(self.global_screen)

            font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 36)  # type: ignore
            margin = 10
            # draw level at top left
            text = font.render(f"Level: {level}", True, (255, 255, 255))
            self.global_screen.blit(text, (margin, margin))  # 10 pixels margin

            # draw score at top right
            text = font.render(f"Score: {score}", True, (255, 255, 255))
            self.global_screen.blit(
                text, (screen_w - text.get_width() - margin, margin)
            )

            pygame.display.flip()

            if len(cursor_group) == 0:
                cleanup()
                return score

            if len(sunflower_group) == 0:
                cleanup()
                return score

    def run(self):
        while True:
            score = self.game_round()

            # if window shut down during game round, return instead of showing game over screen
            if not pygame.display.get_init():
                return

            old_screen = self.global_screen.copy()

            # Game over screen
            menu = pygame_menu.Menu("Game Over", 300, 400, surface=self.global_screen)
            if score > self.highscore:
                self.highscore = score
                menu.add.label(f"New Highscore: {self.highscore}")
            else:
                menu.add.label(f"Score: {score}")
                menu.add.label(f"Highscore: {self.highscore}")
            menu.add.button("Play Again", action=lambda: menu.disable())
            menu.add.button("Quit", pygame_menu.events.EXIT)  # type: ignore

            menu.mainloop(
                self.global_screen, lambda: self.global_screen.blit(old_screen, (0, 0))
            )


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
