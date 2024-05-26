"""
Spaceships Remaster Main File.
(C) 2024 Quddus Salam - All right reserved.
Do not restribute!
"""

import random
from os import path
import pygame
from sprites.background import Background
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bases.entity import Entity
from utils import render_text_with_outline
from config import (
    ANIMATION_SPEED,
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
    ENEMY_VEL,
    ENEMY_FIRE_ANIMATION_SPEED_INCREMENT,
    WAVE_1_ENEMY_COOLDOWN,
    WAVE_2_ENEMY_COOLDOWN,
    WAVE_3_ENEMY_COOLDOWN,
    WAVE_4_ENEMY_COOLDOWN,
    WAVE_5_ENEMY_COOLDOWN,
    WAVE_1_MAX_ENEMY_COUNT,
    WAVE_2_MAX_ENEMY_COUNT,
    WAVE_3_MAX_ENEMY_COUNT,
    WAVE_4_MAX_ENEMY_COUNT,
    WAVE_5_MAX_ENEMY_COUNT,
    NEW_WAVE_SFX,
)


class Game:
    HEART_IMG_PATH = path.join("src", "assets", "graphics", "static", "heart.png")
    SHIELD_IMG_PATH = path.join("src", "assets", "graphics", "static", "shield.png")

    def __init__(self):
        self.window = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def _handle_text_rendering(self, texts):
        for text, rect_kwargs_dict in texts:
            render_text_with_outline(DOGICA_FONT, text, **rect_kwargs_dict)

    def _handle_wave_change(self, game_tick_seconds):
        return min(int(game_tick_seconds // WAVE_CHANGE_TIME) + 1, 5)

    def _handle_new_wave(self, game_tick_seconds, enemy_group, enemy_bullet_group):
        if game_tick_seconds < WAVE_CHANGE_TIME * 5:
            if game_tick_seconds % WAVE_CHANGE_TIME == 0:
                NEW_WAVE_SFX.play()
                enemy_bullet_group.empty()
                enemy_group.empty()

    def _handle_enemy_spawn(
        self,
        game_wave,
        game_tick_seconds,
        enemy_bullet_group,
        drop_group,
        player_sprite,
        enemy_group,
    ):
        random_x_pos = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE[0])
        random_enemy_type = random.choice(ENEMY_TYPES)
        wave_cooldowns = {
            1: WAVE_1_ENEMY_COOLDOWN,
            2: WAVE_2_ENEMY_COOLDOWN,
            3: WAVE_3_ENEMY_COOLDOWN,
            4: WAVE_4_ENEMY_COOLDOWN,
            5: WAVE_5_ENEMY_COOLDOWN,
        }
        wave_max_enemy_counts = {
            1: WAVE_1_MAX_ENEMY_COUNT,
            2: WAVE_2_MAX_ENEMY_COUNT,
            3: WAVE_3_MAX_ENEMY_COUNT,
            4: WAVE_4_MAX_ENEMY_COUNT,
            5: WAVE_5_MAX_ENEMY_COUNT,
        }
        enemy_sprite_only_group = [
            enemy_sprite
            for enemy_sprite in enemy_group
            if enemy_sprite.__class__.__name__ == "Enemy"
        ]  # Since we put health-bar sprite into the same group, we need to separate it with the actual enemy sprite.
        if (
            game_tick_seconds % wave_cooldowns[game_wave] == 0
            and len(enemy_sprite_only_group) < wave_max_enemy_counts[game_wave]
        ):
            Enemy(
                ENEMY_VEL,
                ANIMATION_SPEED + ENEMY_FIRE_ANIMATION_SPEED_INCREMENT * game_wave,
                (random_x_pos, -ENEMY_SIZE[0]),
                enemy_bullet_group,
                drop_group,
                player_sprite,
                random_enemy_type,
                enemy_group,
            )

    def _handle_player_stats_change(self, game_wave, player_sprite):
        player_sprite.update_stats(game_wave)

    def _update_indicator_group(self, current_value, group, image_path, offset_y):
        for entity_sprite in group:
            entity_sprite.kill()
        for i in range(current_value):
            Entity(
                pygame.image.load(image_path).convert_alpha(),
                group,
                topleft=(i * DROP_SIZE[0], offset_y),
            )

    def _handle_heart_and_shield_indicator(
        self, current_health, health_group, current_shield, shield_group
    ):
        self._update_indicator_group(
            current_health, health_group, self.HEART_IMG_PATH, 0
        )
        self._update_indicator_group(
            current_shield, shield_group, self.SHIELD_IMG_PATH, DROP_SIZE[1]
        )

    def _handle_groups(self, *groups):
        for group in groups:
            group.draw(self.window)
            group.update()

    def run(self):
        # Game variables
        game_tick = 0
        game_tick_seconds = 0
        game_wave = 1
        killed_enemies = 0
        running = True

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
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == ENEMY_PASSING_EVENT:
                    ENERGY_ORB_SFX.play()
                    player_sprite.update_shield(-1)
                    enemy_bullet_group.empty()
                elif event.type == GAME_OVER_EVENT:
                    running = False
                elif event.type == ENEMY_KILLED_EVENT:
                    killed_enemies += 1

            # Draw and update functions
            self._handle_heart_and_shield_indicator(
                player_sprite.health_bar.current_health,
                health_group,
                player_sprite.current_shield,
                shield_group,
            )
            self._handle_groups(
                background_group,
                player_group,
                enemy_group,
                player_bullet_group,
                enemy_bullet_group,
                health_group,
                shield_group,
                drop_group,
            )

            # Game logic functions
            game_tick += 1
            game_tick_seconds = game_tick / FPS
            game_wave = self._handle_wave_change(game_tick_seconds)
            self._handle_player_stats_change(game_wave, player_sprite)
            self._handle_enemy_spawn(
                game_wave,
                game_tick_seconds,
                enemy_bullet_group,
                drop_group,
                player_sprite,
                enemy_group,
            )
            self._handle_new_wave(game_tick_seconds, enemy_group, enemy_bullet_group)
            self._handle_text_rendering(
                [
                    (
                        f"Wave {game_wave}",
                        {"center": (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)},
                    ),
                    (
                        str(int(game_tick_seconds)),
                        {
                            "center": (
                                WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 4 + FONT_SIZE * 1.5,
                            )
                        },
                    ),
                    (
                        f"{killed_enemies} Enemies Killed",
                        {"bottomleft": (0, WINDOW_HEIGHT)},
                    ),
                    (
                        "(C) Quddus Salam",
                        {"bottomright": (WINDOW_WIDTH, WINDOW_HEIGHT)},
                    ),
                ]
            )

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        quit(0)


if __name__ == "__main__":
    Game().run()
