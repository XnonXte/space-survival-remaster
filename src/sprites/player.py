from os import path
import pygame
from sprites.bases import movable_animated_entity
from sprites.bullet import PlayerBullet
from utils import load_spritesheet
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_SIZE,
    PLAYER_VEL,
    PLAYER_MAX_HEALTH,
    PLAYER_MAX_SHIELD,
    ENEMY_MAX_HEALTH,
    ENEMY_COLLISION_DAMAGE,
    ANIMATION_SPEED,
    GAME_OVER_EVENT,
    EXPLODE_SFX,
    PLAYER_GUN_SHOT_SFX,
    FLASH_STEP_FRAME,
    ALPHA_MAX,
    ALPHA_TRANSPARENT,
    PLAYER_INVISIBILITY_ENEMY_COLLISION_COUNTDOWN,
)


class Player(movable_animated_entity.MoveableAnimatedLivingEntity):
    IDLING_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "player", "idling")
    )
    FIRING_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "player", "firing")
    )
    MOVING_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "player", "moving")
    )

    def __init__(self, player_bullet_group, enemy_group, group):
        self.firing = False
        self.firing_frame_time = 0
        self.player_bullet_group = player_bullet_group
        self.enemy_group = enemy_group
        self.current_shield = PLAYER_MAX_SHIELD
        self.invisibility_countdown = 0

        #! The callback is temporary!
        super().__init__(
            PLAYER_VEL,
            self.IDLING_SPRITESHEET,
            PLAYER_MAX_HEALTH,
            PLAYER_MAX_HEALTH,
            group,
            "green",
            "bottom",
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE[0]),
        )

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
        # If still firing, ignore input.
        if self.firing:
            return

        PLAYER_GUN_SHOT_SFX.play()
        PlayerBullet(self.rect.midtop, self.enemy_group, self.player_bullet_group)
        self.firing = True

    def _handle_firing_state(self):
        if self.firing:
            self.firing_frame_time += ANIMATION_SPEED
            if self.firing_frame_time >= len(self.spritesheet):
                self.firing = False
                self.firing_frame_time = 0

    def _handle_enemy_collision(self):
        if self.invisibility_countdown > 0:
            return
        for enemy_sprite in self.enemy_group:
            # Since we put the health-bar of enemy into the same group, we need to check if the name the class is "Enemy".
            if (
                pygame.sprite.collide_mask(self, enemy_sprite)
                and enemy_sprite.__class__.__name__ == "Enemy"
            ):
                self.invisibility_countdown = (
                    PLAYER_INVISIBILITY_ENEMY_COLLISION_COUNTDOWN
                )
                enemy_sprite.update_health(-ENEMY_MAX_HEALTH)
                self.update_health(-ENEMY_COLLISION_DAMAGE)

    def _handle_dying(self):
        if self.health_bar.current_health <= 0:
            EXPLODE_SFX.play()
            pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
            self.health_bar.kill()
            self.kill()

    def _handle_invisibility_frames(self):
        """Handling enemy flash when hit."""
        if self.invisibility_countdown > 0:
            if self.invisibility_countdown % FLASH_STEP_FRAME == 0:
                for sprite in self.spritesheet:
                    sprite.set_alpha(ALPHA_MAX)
            else:
                for sprite in self.spritesheet:
                    sprite.set_alpha(ALPHA_TRANSPARENT)
            self.invisibility_countdown -= 1
        else:
            for sprite in self.spritesheet:
                if sprite.get_alpha() != ALPHA_MAX:
                    sprite.set_alpha(ALPHA_MAX)

    def update_shield(self, amount):
        self.current_shield += amount
        if self.current_shield <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
        if self.current_shield >= PLAYER_MAX_SHIELD:
            self.current_shield = PLAYER_MAX_SHIELD

    def update(self):
        super().update()
        self._handle_firing_click()
        self._handle_firing_state()
        self._handle_animation_state()
        self._handle_enemy_collision()
        self._handle_dying()
        self._handle_invisibility_frames()
