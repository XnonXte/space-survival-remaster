import pygame
from os import path
from . import base, bullet
from utils import load_spritesheet, rotate_spritesheet
from constants import (
    WINDOW_HEIGHT,
    ENEMY_VEL,
    ENEMY_BULLET_COOLDOWN,
    ENEMY_PASSING_EVENT,
    ENEMY_MAX_HEALTH,
    ANIMATION_SPEED,
)


class Enemy(base.AnimatedEntity):
    def __init__(self, pos, enemy_bullet_group, player_sprite, enemy_type, group):
        if enemy_type not in ["black", "blue", "green", "red", "red_longwing"]:
            raise Exception("Not a valid enemy type!")
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
        self.health = ENEMY_MAX_HEALTH
        self.firing = False
        self.last_firing_time = 0
        self.firing_frame_time = 0
        self.player_sprite = player_sprite
        self.enemy_bullet_group = enemy_bullet_group

    def _handle_firing(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_firing_time > ENEMY_BULLET_COOLDOWN:
            self.firing = True
            bullet.EnemyBullet(
                self.rect.midbottom, self.player_sprite, self.enemy_bullet_group
            )
            self.last_firing_time = current_time

    def _handle_movement(self):
        self.rect.y += ENEMY_VEL
        if self.rect.top >= WINDOW_HEIGHT:
            pygame.event.post(pygame.event.Event(ENEMY_PASSING_EVENT))
            self.kill()

    def _handle_animation_state(self):
        if self.firing:
            self.spritesheet = self.firing_spritesheet
        else:
            self.spritesheet = self.moving_spritesheet

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
        self._handle_movement()
        self._handle_firing()
        self._handle_animation_state()
        self._handle_firing_state()
