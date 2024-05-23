import pygame

from .animated_entities import AnimatedEntity, AnimatedLivingEntity
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class MoveableAnimatedEntity(AnimatedEntity):
    def __init__(self, vel, initial_spritesheet, group, **rect_kwargs):
        self.vel = vel
        self.direction = pygame.math.Vector2()
        super().__init__(initial_spritesheet, group, **rect_kwargs)

    def _handle_y_movement(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.direction.y = -1
        elif keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def _handle_x_movement(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.direction.x = -1
        elif keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def _normalize_vector(self):
        if self.direction.length() > 0:
            self.direction.normalize_ip()

    def _handle_movement(self):
        keys = pygame.key.get_pressed()

        # Handling x and y movements, also check if the entity is inside the boundary.
        self._handle_y_movement(keys)
        self._handle_x_movement(keys)

        # Normal diagonal speed.
        self._normalize_vector()

        self._apply_movement()

    def _apply_movement(self):
        self.rect.center += self.direction * self.vel

    def update(self):
        super().update()
        self._handle_movement()


class MoveableAnimatedLivingEntity(AnimatedLivingEntity):
    def __init__(
        self,
        vel,
        initial_spritesheet,
        max_health,
        current_health,
        group,
        dying_callback,
        health_bar_color,
        health_bar_pos,
        **rect_kwargs,
    ):
        self.vel = vel
        self.direction = pygame.math.Vector2()
        super().__init__(
            initial_spritesheet,
            max_health,
            current_health,
            group,
            dying_callback,
            health_bar_color,
            health_bar_pos,
            **rect_kwargs,
        )

    def _handle_y_movement(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.direction.y = -1
        elif keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def _handle_x_movement(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.direction.x = -1
        elif keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def _normalize_vector(self):
        if self.direction.length() > 0:
            self.direction.normalize_ip()

    def _handle_movement(self):
        keys = pygame.key.get_pressed()

        # Handling x and y movements, also check if the entity is inside the boundary.
        self._handle_y_movement(keys)
        self._handle_x_movement(keys)

        # Normal diagonal speed.
        self._normalize_vector()

        self._apply_movement()

    def _apply_movement(self):
        self.rect.center += self.direction * self.vel

    def update(self):
        super().update()
        self._handle_movement()
