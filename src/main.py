# TODO: Create simple UI for: score, wave, etc.
# TODO: Create a wave system which uses the game's tick.
# TODO: Create a simple main menu? (https://youtu.be/2iyx8_elcYg?si=RjqQtYt5eEmDjyrb)
# TODO: Store score in a JSON file.

import pygame
import random
from os import path

from config import window, clock
from sprites.background import Background
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bases.entity import Entity
from constants import (
    ENEMY_SPAWN_EVENT,
    ENEMY_SPAWN_COOLDOWN,
    WINDOW_WIDTH,
    ENEMY_TYPES,
    ENEMY_SIZE,
    ENEMY_PASSING_EVENT,
    GAME_OVER_EVENT,
    FPS,
    DROP_SIZE,
)


class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

    def _draw_shield_count(self, current_shield, shield_group):
        for entity_sprite in shield_group:
            entity_sprite.kill()
        for i in range(current_shield):
            Entity(
                pygame.image.load(
                    path.join("src", "assets", "graphics", "static", "shield.png")
                ).convert_alpha(),
                shield_group,
                topleft=(WINDOW_WIDTH - DROP_SIZE[0] - i * DROP_SIZE[0], 0),
            )

    def _draw_health_count(self, current_health, health_group):
        for entity_sprite in health_group:
            entity_sprite.kill()
        for i in range(current_health):
            Entity(
                pygame.image.load(
                    path.join("src", "assets", "graphics", "static", "heart.png")
                ).convert_alpha(),
                health_group,
                topleft=(i * DROP_SIZE[0], 0),
            )

    def _draw_and_update_groups(self, *groups):
        for group in groups:
            group.draw(self.window)
            group.update()

    def run(self):
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_COOLDOWN)

        # Groups.
        background_group = pygame.sprite.GroupSingle()
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        enemy_bullet_group = pygame.sprite.Group()
        player_bullet_group = pygame.sprite.Group()
        health_group = pygame.sprite.Group()
        shield_group = pygame.sprite.Group()
        drop_group = pygame.sprite.Group()

        # Sprites.
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
                        drop_group,
                        player_sprite,
                        random_enemy_type,
                        enemy_group,
                    )
                if event.type == ENEMY_PASSING_EVENT:
                    player_sprite.update_shield(-1)
                if event.type == GAME_OVER_EVENT:
                    #! Temporary.
                    running = False

            self.window.fill("black")
            self._draw_health_count(
                player_sprite.health_bar.current_health, health_group
            )
            self._draw_shield_count(player_sprite.current_shield, shield_group)
            self._draw_and_update_groups(
                background_group,
                player_group,
                enemy_group,
                player_bullet_group,
                enemy_bullet_group,
                health_group,
                shield_group,
                drop_group,
            )
            pygame.display.flip()
            self.clock.tick(FPS)

        # Cleanup after game quit.
        pygame.quit()
        quit(0)


if __name__ == "__main__":
    game = Game(window, clock)
    game.run()
