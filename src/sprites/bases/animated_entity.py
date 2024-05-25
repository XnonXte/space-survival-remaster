import pygame
from .entity import Entity, LivingEntity
from config import ANIMATION_SPEED


class AnimatedEntity(Entity):
    def __init__(self, initial_spritesheet, group, **rect_kwargs):
        self.animation_index = 0
        self.spritesheet = initial_spritesheet
        self.last_frame_spritesheet = self.spritesheet
        image = self.spritesheet[self.animation_index]
        super().__init__(image, group, **rect_kwargs)

    def _handle_animation(self):
        self.animation_index += ANIMATION_SPEED
        if (
            self.spritesheet != self.last_frame_spritesheet
            or self.animation_index >= len(self.spritesheet)
        ):
            self.animation_index = 0
        self.image = self.spritesheet[int(self.animation_index)]
        self.last_frame_spritesheet = self.spritesheet

    def _update_rect_and_mask(self):
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._handle_animation()
        self._update_rect_and_mask()


class AnimatedLivingEntity(LivingEntity):
    def __init__(
        self,
        initial_spritesheet,
        max_health,
        current_health,
        group,
        health_bar_color,
        health_bar_pos,
        **rect_kwargs,
    ):
        self.animation_index = 0
        self.spritesheet = initial_spritesheet
        self.last_frame_spritesheet = self.spritesheet
        image = self.spritesheet[self.animation_index]
        super().__init__(
            max_health,
            current_health,
            image,
            group,
            health_bar_color,
            health_bar_pos,
            **rect_kwargs,
        )

    def _handle_animation(self):
        self.animation_index += ANIMATION_SPEED
        if (
            self.spritesheet != self.last_frame_spritesheet
            or self.animation_index >= len(self.spritesheet)
        ):
            self.animation_index = 0
        self.image = self.spritesheet[int(self.animation_index)]
        self.last_frame_spritesheet = self.spritesheet

    def _update_rect_and_mask(self):
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self._handle_animation()
        self._update_rect_and_mask()
