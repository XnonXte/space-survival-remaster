# TODO: Implement a wave mechanism.
# TODO: Create a simple main menu? (https://youtu.be/2iyx8_elcYg?si=RjqQtYt5eEmDjyrb)
# TODO: Store score in a JSON file.
# TODO: The main menu should consist of a history and a play button.

import random
from os import path
import pygame
from sprites.background import Background
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bases.entity import Entity
from utils import render_text_with_outline
from config import (
    ENEMY_SPAWN_EVENT,
    ENEMY_SPAWN_COOLDOWN,
    FONT_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    ENEMY_TYPES,
    ENEMY_SIZE,
    ENEMY_PASSING_EVENT,
    GAME_OVER_EVENT,
    FPS,
    DROP_SIZE,
    DOGICA_FONT,
    WAVE_CHANGE_TIME,
    ENEMY_KILLED_EVENT,
    ENERGY_ORB_SFX,
)


class Game:
    def __init__(self):
        self.window = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def _render_texts(self, texts):
        for text, rect_kwargs_dict in texts:
            render_text_with_outline(DOGICA_FONT, text, **rect_kwargs_dict)

    def _update_game_tick(self):
        return pygame.time.get_ticks()

    def _determine_game_wave(self, game_tick):
        if game_tick <= WAVE_CHANGE_TIME * 1.0:
            return 1
        elif game_tick <= WAVE_CHANGE_TIME * 2.0:
            return 2
        elif game_tick <= WAVE_CHANGE_TIME * 3.0:
            return 3
        elif game_tick <= WAVE_CHANGE_TIME * 4.0:
            return 4
        elif game_tick <= WAVE_CHANGE_TIME * 5.0:
            return 5

    def _handle_wave_change(self, game_tick):
        # TODO: Implement this as well.
        ...

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

    def _draw_shield_count(self, current_shield, shield_group):
        for entity_sprite in shield_group:
            entity_sprite.kill()
        for i in range(current_shield):
            Entity(
                pygame.image.load(
                    path.join("src", "assets", "graphics", "static", "shield.png")
                ).convert_alpha(),
                shield_group,
                topleft=(i * DROP_SIZE[0], DROP_SIZE[1]),
            )

    def _draw_and_update_groups(self, *groups):
        for group in groups:
            group.draw(self.window)
            group.update()

    def run(self):
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_COOLDOWN)
        background_group = pygame.sprite.GroupSingle()
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        enemy_bullet_group = pygame.sprite.Group()
        player_bullet_group = pygame.sprite.Group()
        health_group = pygame.sprite.Group()
        shield_group = pygame.sprite.Group()
        drop_group = pygame.sprite.Group()
        Background(background_group)
        player_sprite = Player(player_bullet_group, enemy_group, player_group)

        # Game variables.
        game_tick = 0
        game_wave = 1
        killed_enemies = 0

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
                    ENERGY_ORB_SFX.play()
                    player_sprite.update_shield(-1)
                    enemy_bullet_group.empty()
                if event.type == GAME_OVER_EVENT:
                    #! Temporary.
                    running = False
                if event.type == ENEMY_KILLED_EVENT:
                    killed_enemies += 1

            # Draw functions.
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

            # Game logics.
            game_tick = self._update_game_tick()
            game_wave = self._determine_game_wave(game_tick)
            self._handle_wave_change(game_tick)
            self._render_texts(
                [
                    (
                        f"Wave {game_wave}",
                        {"center": (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)},
                    ),
                    (
                        str(int(game_tick / 1000)),
                        {
                            "center": (
                                WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 4 + FONT_SIZE * 1.5,
                            )
                        },
                    ),
                    (
                        f"{killed_enemies} Enemies Killed",
                        {"bottomright": (WINDOW_WIDTH, WINDOW_HEIGHT)},
                    ),
                    (
                        "(C) Quddus Salam",
                        {"bottomleft": (0, WINDOW_HEIGHT - FONT_SIZE * 1.5)},
                    ),
                    (
                        "Do not redistribute!",
                        {"bottomleft": (0, WINDOW_HEIGHT)},
                    ),
                ]
            )

            # Updating display and setting up a constant tickrate.
            pygame.display.flip()
            self.clock.tick(FPS)

        # Cleanup after game quit.
        pygame.quit()
        quit(0)


if __name__ == "__main__":
    Game().run()
