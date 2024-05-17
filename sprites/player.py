import pygame
from os import path
from . import base, bullet
from utils import load_spritesheet
from constants import (
    PLAYER_VEL,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


class Player(base.MoveableAnimatedEntity):
    IDLING_SPRITESHEET = load_spritesheet(
        path.join("assets", "graphics", "player", "idling")
    )
    FIRING_SPRITESHEET = load_spritesheet(
        path.join("assets", "graphics", "player", "firing")
    )
    MOVING_SPRITESHEET = load_spritesheet(
        path.join("assets", "graphics", "player", "moving")
    )

    def __init__(self, player_bullet_group, enemy_group, group):
        super().__init__(
            PLAYER_VEL,
            self.IDLING_SPRITESHEET,
            group,
            center=(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT - self.IDLING_SPRITESHEET[0].get_height(),
            ),
        )
        self.firing = False
        self.last_firing_time = 0
        self.player_bullet_group = player_bullet_group
        self.enemy_group = enemy_group

    def _handle_animation_state(self):
        if self.firing:
            self.spritesheet = self.FIRING_SPRITESHEET
        elif self.direction.x != 0 or self.direction.y != 0:
            self.spritesheet = self.MOVING_SPRITESHEET
        else:
            self.spritesheet = self.IDLING_SPRITESHEET

    def _handle_firing_state(self):
        if self.firing and self.animation_index >= len(self.spritesheet):
            self.firing = False

    def fire(self):
        current_time = pygame.time.get_ticks()
        if current_time < self.last_firing_time:
            return
        bullet.PlayerBullet(
            self.rect.midtop, self.enemy_group, self.player_bullet_group
        )
        self.last_firing_time = current_time

    def damage(self):
        print("TODO: Implement damage mechanism")

    def update(self):
        super().update()
        self._handle_animation_state()
        self._handle_animation()
        self._handle_firing_state()
