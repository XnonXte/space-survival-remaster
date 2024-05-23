# TODO: Implement a healthbar indicator on the top left, and shield indicator on the top right.
# TODO: Add heart-drop and shield-drop?
# TODO: Create simple UI for: bullets, score, wave, etc.
# TODO: Create a wave system which uses the game's tick.
# TODO: Create a simple main menu? (https://youtu.be/2iyx8_elcYg?si=RjqQtYt5eEmDjyrb)
# TODO: Store score in a JSON file.

import pygame
import random

from config import *
from constants import *
from sprites import *


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

    def draw_and_update_groups(self, *groups):
        for group in groups:
            if not hasattr(group, "draw") and not hasattr(group, "update"):
                raise Exception("Not a valid group!")
            group.draw(self.window)
            group.update()

    def run(self):
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_COOLDOWN)
        background_group = pygame.sprite.GroupSingle()
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        enemy_bullet_group = pygame.sprite.Group()
        player_bullet_group = pygame.sprite.Group()
        Background(background_group)
        player_sprite = Player(player_bullet_group, enemy_group, player_group)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == ENEMY_SPAWN_EVENT:
                    random_x_pos = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE[0])
                    random_enemy_type = random.choice(ENEMY_TYPES)
                    Enemy(
                        (random_x_pos, -ENEMY_SIZE[1]),
                        enemy_bullet_group,
                        player_sprite,
                        random_enemy_type,
                        enemy_group,
                    )
                if event.type == ENEMY_PASSING_EVENT:
                    # TODO: Implemeny enemy passing event.
                    ...
            self.window.fill("black")
            self.draw_and_update_groups(
                background_group,
                player_group,
                enemy_group,
                player_bullet_group,
                enemy_bullet_group,
            )
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        quit(0)


if __name__ == "__main__":
    game = Game(window, clock)
    game.run()
