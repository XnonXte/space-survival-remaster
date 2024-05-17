import pygame
from os import path
from . import base, bullet
from utils import load_spritesheet, rotate_spritesheet
from constants import (
    ENEMY_VEL,
    ENEMY_BULLET_COOLDOWN,
    WINDOW_HEIGHT,
    ENEMY_PASSING_EVENT,
)


class Enemy(base.AnimatedEntity):
    def __init__(self, pos, enemy_bullet_group, player_sprite, enemy_type, group):

        # Safety check.
        if enemy_type not in ["black", "blue", "green", "red", "red_longwing"]:
            raise NotImplemented

        self.moving_spritesheet = rotate_spritesheet(
            load_spritesheet(
                path.join("assets", "graphics", "enemies", enemy_type, "moving")
            ),
            180,
        )
        self.firing_spritesheet = rotate_spritesheet(
            load_spritesheet(
                path.join("assets", "graphics", "enemies", enemy_type, "firing")
            ),
            180,
        )
        super().__init__(self.moving_spritesheet, group, topleft=pos)
        self.firing = False
        self.last_firing_time = 0
        self.player_sprite = player_sprite
        self.enemy_bullet_group = enemy_bullet_group

    def _handle_firing(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_firing_time > ENEMY_BULLET_COOLDOWN:
            bullet.EnemyBullet(
                self.rect.midbottom, self.player_sprite, self.enemy_bullet_group
            )
            self.last_firing_time = current_time

    def _handle_movement(self):
        self.rect.y += ENEMY_VEL
        if self.rect.top >= WINDOW_HEIGHT:
            pygame.event.post(pygame.event.Event(ENEMY_PASSING_EVENT))
            self.kill()

    def _handle_firing_state(self):
        if self.firing and self.animation_index >= len(self.spritesheet):
            self.firing = False
        if self.firing:
            self.spritesheet = self.firing_spritesheet
        else:
            self.spritesheet = self.moving_spritesheet

    def update(self):
        super().update()
        self._handle_firing()
        self._handle_movement()
        self._handle_firing_state()
