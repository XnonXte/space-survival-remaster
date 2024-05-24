import pygame
from os import path

from sprites.bases import animated_entity
from constants import DROP_TIMEOUT, DROP_TYPE
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
            raise Exception("Invalid drop-type!")
        self.player_sprite = player_sprite
        self.created_time = pygame.time.get_ticks()
        super().__init__(self.HEART_SPRITESHEET, group, topleft=pos)

    def _handle_player_collision(self):
        if pygame.sprite.collide_mask(self, self.player_sprite):
            self.player_sprite.update_health(1)
            self.kill()

    def _handle_timeout(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= DROP_TIMEOUT:
            self.kill()

    def update(self):
        super().update()
        self._handle_player_collision()
        self._handle_timeout()
