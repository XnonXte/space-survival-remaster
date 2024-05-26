import random
from os import path
import pygame
from sprites.bases import animated_entity
from sprites.bullet import EnemyBullet
from sprites.drop import Drop
from utils import load_spritesheet, rotate_spritesheet
from config import (
    DROP_TYPE,
    WINDOW_HEIGHT,
    ENEMY_BULLET_COOLDOWN,
    ENEMY_PASSING_EVENT,
    ENEMY_MAX_HEALTH,
    ANIMATION_SPEED,
    DROP_CHANCE,
    EXPLODE_SFX,
    ENEMY_GUN_SHOT_SFX,
    ENEMY_KILLED_EVENT,
    PLAYER_MAX_HEALTH,
    PLAYER_MAX_SHIELD,
    ENEMY_TYPES,
)


class Enemy(animated_entity.AnimatedLivingEntity):
    def __init__(
        self,
        vel,
        fire_animation_speed,
        pos,
        enemy_bullet_group,
        drop_group,
        player_sprite,
        enemy_type,
        group,
    ):
        if enemy_type not in ENEMY_TYPES:
            raise ValueError(f"'{enemy_type}' is not a valid enemy type!")
        self.moving_spritesheet = self._load_and_rotate_spritesheet(
            enemy_type, "moving"
        )
        self.firing_spritesheet = self._load_and_rotate_spritesheet(
            enemy_type, "firing"
        )
        self.vel = vel
        self.fire_animation_speed = fire_animation_speed
        self.firing = False
        self.last_firing_time = 0
        self.firing_frame_time = 0
        self.player_sprite = player_sprite
        self.enemy_bullet_group = enemy_bullet_group
        self.drop_group = drop_group
        super().__init__(
            self.moving_spritesheet,
            ENEMY_MAX_HEALTH,
            ENEMY_MAX_HEALTH,
            group,
            "green",
            "top",
            topleft=pos,
        )

    def _load_and_rotate_spritesheet(self, enemy_type, action):
        return rotate_spritesheet(
            load_spritesheet(
                path.join("src", "assets", "graphics", "enemies", enemy_type, action)
            ),
            180,
        )

    def _handle_firing(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_firing_time >= ENEMY_BULLET_COOLDOWN:
            ENEMY_GUN_SHOT_SFX.play()
            self.firing = True
            EnemyBullet(
                self.rect.midbottom, self.player_sprite, self.enemy_bullet_group
            )
            self.last_firing_time = current_time

    def _handle_movement(self):
        self.rect.y += self.vel
        if self.rect.top >= WINDOW_HEIGHT:
            pygame.event.post(pygame.event.Event(ENEMY_PASSING_EVENT))
            self.health_bar.kill()
            self.kill()

    def _handle_animation_state(self):
        self.spritesheet = (
            self.firing_spritesheet if self.firing else self.moving_spritesheet
        )

    def _handle_firing_state(self):
        if self.firing:
            self.firing_frame_time += ANIMATION_SPEED
            if self.firing_frame_time >= len(self.spritesheet):
                self.firing = False
                self.firing_frame_time = 0

    def _handle_drop(self):
        if random.randint(1, 100) <= DROP_CHANCE:
            if (
                self.player_sprite.health_bar.current_health < PLAYER_MAX_HEALTH
                or self.player_sprite.current_shield < PLAYER_MAX_SHIELD
            ):
                drop_type = self._determine_drop_type()
                Drop(self.rect.topleft, drop_type, self.player_sprite, self.drop_group)

    def _determine_drop_type(self):
        if (
            self.player_sprite.health_bar.current_health < PLAYER_MAX_HEALTH
            and self.player_sprite.current_shield < PLAYER_MAX_SHIELD
        ):
            return random.choice(DROP_TYPE)
        elif self.player_sprite.health_bar.current_health < PLAYER_MAX_HEALTH:
            return "heart"
        elif self.player_sprite.current_shield < PLAYER_MAX_SHIELD:
            return "shield"
        else:
            return None

    def _handle_dying(self):
        if self.health_bar.current_health <= 0:
            EXPLODE_SFX.play()
            pygame.event.post(pygame.event.Event(ENEMY_KILLED_EVENT))
            self._handle_drop()
            self.health_bar.kill()
            self.kill()

    def _handle_firing_speed(self):
        self.animation_speed = (
            self.fire_animation_speed if self.firing else ANIMATION_SPEED
        )

    def update(self):
        super().update()
        self._handle_movement()
        self._handle_firing()
        self._handle_animation_state()
        self._handle_firing_state()
        self._handle_dying()
        self._handle_firing_speed()
