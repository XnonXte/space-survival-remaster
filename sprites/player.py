import pygame
from os import path
from . import base, bullet
from utils import load_spritesheet
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_SIZE,
    PLAYER_VEL,
    PLAYER_MAX_HEALTH,
    ANIMATION_SPEED,
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
                WINDOW_HEIGHT - PLAYER_SIZE[0],
            ),
        )
        self.health = PLAYER_MAX_HEALTH
        self.firing = False
        self.firing_frame_time = 0
        self.player_bullet_group = player_bullet_group
        self.enemy_group = enemy_group

    def _handle_animation_state(self):
        if self.firing:
            self.spritesheet = self.FIRING_SPRITESHEET
        elif self.direction.x != 0 or self.direction.y != 0:
            self.spritesheet = self.MOVING_SPRITESHEET
        else:
            self.spritesheet = self.IDLING_SPRITESHEET

    def _handle_firing_click(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._handle_firing()

    def _handle_firing(self):
        if not self.firing:
            bullet.PlayerBullet(
                self.rect.midtop, self.enemy_group, self.player_bullet_group
            )
            self.firing = True

    def _handle_firing_state(self):
        if self.firing:
            self.firing_frame_time += ANIMATION_SPEED
            if self.firing_frame_time >= len(self.spritesheet):
                self.firing = False
                self.firing_frame_time = 0

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def update(self):
        super().update()
        self._handle_firing_click()
        self._handle_firing_state()
        self._handle_animation_state()
