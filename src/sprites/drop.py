from os import path
import pygame
from sprites.bases import animated_entity
from config import DROP_TIMEOUT, DROP_TYPE, HEART_DROP_SFX, SHIELD_DROP_SFX
from utils import load_spritesheet


class Drop(animated_entity.AnimatedEntity):
    HEART_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "items", "heart")
    )
    SHIELD_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "items", "shield")
    )

    def __init__(self, pos, drop_type, player_sprite, group):
        if drop_type not in DROP_TYPE:
            raise ValueError(f"'{drop_type}' is not a valid drop type!")
        self.drop_type = drop_type
        self.player_sprite = player_sprite
        self.created_time = pygame.time.get_ticks()
        spritesheet = (
            self.HEART_SPRITESHEET if drop_type == "heart" else self.SHIELD_SPRITESHEET
        )
        super().__init__(spritesheet, group, topleft=pos)

    def _handle_player_collision(self):
        """Handle collision with the player sprite."""
        if pygame.sprite.collide_mask(self, self.player_sprite):
            if self.drop_type == "heart":
                HEART_DROP_SFX.play()
                self.player_sprite.update_health(1)
            else:
                SHIELD_DROP_SFX.play()
                self.player_sprite.update_shield(1)
            self.kill()

    def _handle_timeout(self):
        """Remove the drop after a certain timeout period."""
        if pygame.time.get_ticks() - self.created_time >= DROP_TIMEOUT:
            self.kill()

    def update(self):
        """Update the drop's state."""
        super().update()
        self._handle_player_collision()
        self._handle_timeout()
