import pygame
from os import path
from . import base
from utils import load_spritesheet, rotate_spritesheet
from constants import (
    PLAYER_BULLET_VEL,
    ENEMY_BULLET_VEL,
    WINDOW_HEIGHT,
    PLAYER_BULLET_DAMAGE,
    ENEMY_BULLET_DAMAGE,
)


class PlayerBullet(base.AnimatedEntity):
    BULLET_SPRITESHEET = load_spritesheet(
        path.join("assets", "graphics", "bullets", "player")
    )

    def __init__(self, pos, enemy_group, group):
        super().__init__(self.BULLET_SPRITESHEET, group, midbottom=pos)
        self.enemy_group = enemy_group

    def _handle_movement(self):
        self.rect.y -= PLAYER_BULLET_VEL
        if self.rect.bottom <= 0:
            self.kill()

    def _handle_enemy_impact(self):
        for enemy_sprite in self.enemy_group:
            if pygame.sprite.collide_mask(self, enemy_sprite):
                enemy_sprite.damage()
                self.kill()

    def update(self):
        super().update()
        self._handle_movement()
        self._handle_enemy_impact()


class EnemyBullet(base.AnimatedEntity):
    ENEMY_BULLET_SPRITESHEET = rotate_spritesheet(
        load_spritesheet(path.join("assets", "graphics", "bullets", "enemy")), 180
    )

    def __init__(self, pos, player_sprite, group):
        super().__init__(self.ENEMY_BULLET_SPRITESHEET, group, midtop=pos)
        self.player_sprite = player_sprite

    def _handle_movement(self):
        self.rect.y += ENEMY_BULLET_VEL
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()

    def _handle_player_impact(self):
        if pygame.sprite.collide_mask(self, self.player_sprite):
            self.player_sprite.damage()
            self.kill()

    def update(self):
        super().update()
        self._handle_movement()
        self._handle_player_impact()
