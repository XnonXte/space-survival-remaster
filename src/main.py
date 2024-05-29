"""
Spaceships Remaster Main File.
(C) 2024 Quddus Salam - All right reserved.
Do not restribute!
"""

import random
from os import path
from datetime import datetime
import pygame
from sprites.background import Background
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bases.entity import Entity
from utils import render_text, read_history, save_history
from button import Button
from config import (
    ANIMATION_SPEED,
    BUTTONS_SPACING,
    FONT_SIZE,
    GAME_OVER_CAPTION,
    HISTORY_CAPTION,
    MAIN_MENU_CAPTION,
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
    CAPPED_HISTORY_AMOUNT,
)


class Game:
    HEART_IMG_PATH = path.join("src", "assets", "graphics", "static", "heart.png")
    SHIELD_IMG_PATH = path.join("src", "assets", "graphics", "static", "shield.png")

    def __init__(self):
        self.window = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def _handle_text_rendering(self, texts):
        for text, rect_kwargs_dict in texts:
            render_text(text, DOGICA_FONT, **rect_kwargs_dict)

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

    def _handle_groups(self, groups):
        for group in groups:
            if not hasattr(group, "draw") and not hasattr(group, "update"):
                raise Exception("Invalid group!")
            group.draw(self.window)
            group.update()

    def _handle_buttons(self, mouse_pos, buttons):
        for button in buttons:
            if not hasattr(button, "change_color") and not hasattr(button, "update"):
                raise Exception("Invalid button!")
            button.change_color(mouse_pos)
            button.update(self.window)

    def main_menu(self):
        pygame.display.set_caption(MAIN_MENU_CAPTION)
        backgrond_group = pygame.sprite.GroupSingle()
        Background(backgrond_group)
        while True:
            menu_mouse_pos = pygame.mouse.get_pos()
            play_button = Button(
                None,
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTONS_SPACING),
                "PLAY",
                DOGICA_FONT,
                "white",
                "purple",
            )
            history_button = Button(
                None,
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
                "HISTORY",
                DOGICA_FONT,
                "white",
                "purple",
            )
            quit_button = Button(
                None,
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + BUTTONS_SPACING),
                "QUIT",
                DOGICA_FONT,
                "white",
                "red",
            )
            self.window.fill("black")
            self._handle_groups([backgrond_group])
            self._handle_buttons(
                menu_mouse_pos, [play_button, history_button, quit_button]
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        self.play()
                    if history_button.check_for_input(menu_mouse_pos):
                        self.history()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        quit(0)
            pygame.display.flip()
            self.clock.tick(FPS)

    def history(self):
        pygame.display.set_caption(HISTORY_CAPTION)
        background_group = pygame.sprite.GroupSingle()
        Background(background_group)
        sorted_history = sorted(read_history(), key=lambda h: h["created_at"])
        capped_history = sorted_history[:CAPPED_HISTORY_AMOUNT]
        capped_history_texts = (
            [
                (
                    f"{h['score']} | {h['game_wave']} | {h['enemies_killed']} - {datetime.fromtimestamp(h['created_at']).strftime('%a %d %b, %Y')}",
                    {
                        "center": (
                            WINDOW_WIDTH // 2,
                            WINDOW_HEIGHT // 4 + BUTTONS_SPACING * count,
                        )
                    },
                )
                for count, h in enumerate(capped_history, start=1)
            ]
            if len(sorted_history) != 0
            else [
                (
                    "You haven't played yet!",
                    {
                        "center": (
                            WINDOW_WIDTH // 2,
                            WINDOW_HEIGHT // 4
                            + BUTTONS_SPACING * CAPPED_HISTORY_AMOUNT // 2,
                        )
                    },
                )
            ]
        )
        while True:
            history_mouse_pos = pygame.mouse.get_pos()
            back_button = Button(
                None,
                (
                    WINDOW_WIDTH // 2,
                    WINDOW_HEIGHT // 4 + BUTTONS_SPACING * CAPPED_HISTORY_AMOUNT + 1,
                ),
                "BACK",
                DOGICA_FONT,
                "white",
                "green",
            )
            self.window.fill("black")
            self._handle_groups([background_group])
            self._handle_text_rendering(
                [
                    (
                        "Game History (S, W, EK)",
                        {"center": (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)},
                    ),
                    *capped_history_texts,
                ]
            )
            self._handle_buttons(history_mouse_pos, [back_button])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.check_for_input(history_mouse_pos):
                        self.main_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

    def play(self):
        # Game variables.
        game_tick = 0
        game_tick_seconds = 0
        game_wave = 1
        enemies_killed = 0

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
        while True:
            pygame.display.set_caption(
                f"Score: {int(game_tick_seconds)} | Wave: {game_wave} | Enemies Killed: {enemies_killed}"
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                elif event.type == ENEMY_PASSING_EVENT:
                    ENERGY_ORB_SFX.play()
                    player_sprite.update_shield(-1)
                    enemy_bullet_group.empty()
                elif event.type == GAME_OVER_EVENT:
                    history = read_history()
                    history.append(
                        {
                            "score": int(game_tick_seconds),
                            "game_wave": game_wave,
                            "enemies_killed": enemies_killed,
                            "created_at": datetime.now().timestamp(),
                        }
                    )
                    save_history(history)
                    self.game_over(game_tick_seconds, game_wave, enemies_killed)
                elif event.type == ENEMY_KILLED_EVENT:
                    enemies_killed += 1

            # Draw and update functions
            self.window.fill("black")
            self._handle_heart_and_shield_indicator(
                player_sprite.health_bar.current_health,
                health_group,
                player_sprite.current_shield,
                shield_group,
            )
            self._handle_groups(
                [
                    background_group,
                    player_group,
                    enemy_group,
                    player_bullet_group,
                    enemy_bullet_group,
                    health_group,
                    shield_group,
                    drop_group,
                ]
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
                        f"{enemies_killed} Enemies Killed",
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

    def game_over(self, game_tick_seconds, game_wave, enemies_killed):
        pygame.display.set_caption(GAME_OVER_CAPTION)
        background_group = pygame.sprite.GroupSingle()
        Background(background_group)
        while True:
            game_over_mouse_pos = pygame.mouse.get_pos()
            back_button = Button(
                None,
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + BUTTONS_SPACING * 4),
                "BACK TO MENU",
                DOGICA_FONT,
                "white",
                "green",
            )
            self.window.fill("black")
            self._handle_groups([background_group])
            self._handle_text_rendering(
                [
                    ("Game Over!", {"center": (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)}),
                    (
                        f"Score: {int(game_tick_seconds)}",
                        {
                            "center": (
                                WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 4 + BUTTONS_SPACING,
                            )
                        },
                    ),
                    (
                        f"Game Wave: {game_wave}",
                        {
                            "center": (
                                WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 4 + BUTTONS_SPACING * 2,
                            )
                        },
                    ),
                    (
                        f"Enemies Killed: {enemies_killed}",
                        {
                            "center": (
                                WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 4 + BUTTONS_SPACING * 3,
                            )
                        },
                    ),
                ]
            )
            self._handle_buttons(game_over_mouse_pos, [back_button])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.check_for_input(game_over_mouse_pos):
                        self.main_menu()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().main_menu()
