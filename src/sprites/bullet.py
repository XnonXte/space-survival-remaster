from os import path
import pygame
from sprites.bases import animated_entity
from utils import load_spritesheet, rotate_spritesheet
from config import (
    ENEMY_BULLET_VEL,
    WINDOW_HEIGHT,
    PLAYER_BULLET_DAMAGE,
    ENEMY_BULLET_DAMAGE,
    HIT_MARK_SFX,
    PLAYER_INVISIBILITY_HIT_COUNTDOWN,
)


class PlayerBullet(animated_entity.AnimatedEntity):
    BULLET_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "bullets", "player")
    )

    def __init__(self, vel, pos, enemy_group, group):
        self.vel = vel
        self.enemy_group = enemy_group
        super().__init__(self.BULLET_SPRITESHEET, group, midbottom=pos)

    def _handle_movement(self):
        """Handle the movement of the bullet."""
        self.rect.y -= self.vel
        if self.rect.bottom <= 0:
            self.kill()

    def _handle_enemy_impact(self):
        """Handle the bullet's impact with enemies."""
        for enemy_sprite in self.enemy_group:
            # Check if the bullet collides with an enemy.
            if (
                pygame.sprite.collide_mask(self, enemy_sprite)
                and enemy_sprite.__class__.__name__ == "Enemy"
            ):
                HIT_MARK_SFX.play()
                enemy_sprite.update_health(-PLAYER_BULLET_DAMAGE)
                self.kill()

    def update(self):
        """Update the bullet's state."""
        super().update()
        self._handle_movement()
        self._handle_enemy_impact()


class EnemyBullet(animated_entity.AnimatedEntity):
    ENEMY_BULLET_SPRITESHEET = rotate_spritesheet(
        load_spritesheet(path.join("src", "assets", "graphics", "bullets", "enemy")),
        180,
    )

    def __init__(self, pos, player_sprite, group):
        self.player_sprite = player_sprite
        super().__init__(self.ENEMY_BULLET_SPRITESHEET, group, midtop=pos)

    def _handle_movement(self):
        """Handle the movement of the bullet."""
        self.rect.y += ENEMY_BULLET_VEL
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()

    def _handle_player_impact(self):
        """Handle the bullet's impact with the player."""
        if self.player_sprite.invisibility_countdown > 0:
            return
        if pygame.sprite.collide_mask(self, self.player_sprite):
            HIT_MARK_SFX.play()
            self.player_sprite.invisibility_countdown = (
                PLAYER_INVISIBILITY_HIT_COUNTDOWN
            )
            self.player_sprite.update_health(-ENEMY_BULLET_DAMAGE)
            self.kill()

    def update(self):
        """Update the bullet's state."""
        super().update()
        self._handle_movement()
        self._handle_player_impact()
