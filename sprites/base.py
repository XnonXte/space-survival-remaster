import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, ANIMATION_SPEED


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, group, **rect_kwargs):
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(group)


class AnimatedEntity(Entity):
    def __init__(self, initial_spritesheet, group, **rect_kwargs):
        self.animation_index = 0
        self.spritesheet = initial_spritesheet
        self.last_frame_spritesheet = self.spritesheet
        image = self.spritesheet[self.animation_index]
        super().__init__(image, group, **rect_kwargs)

    def _handle_animation(self):
        self.animation_index += ANIMATION_SPEED
        if self.animation_index >= len(self.spritesheet):
            self.animation_index = 0
        self.image = self.spritesheet[int(self.animation_index)]
        self.last_frame_spritesheet = self.spritesheet

    def update(self):
        self._handle_animation()


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
        self._handle_y_movement(keys)
        self._handle_x_movement(keys)
        self._normalize_vector()
        self._apply_movement()

    def _apply_movement(self):
        self.rect.center += self.direction * self.vel

    def update(self):
        self._handle_movement()
