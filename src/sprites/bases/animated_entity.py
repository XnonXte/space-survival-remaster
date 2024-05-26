import pygame
from .entity import Entity, LivingEntity
from config import ANIMATION_SPEED


class AnimatedEntity(Entity):
    """
    Represents an entity with animation capabilities in the game world.
    """

    def __init__(self, initial_spritesheet, group, **rect_kwargs):
        """
        Initialize an animated entity.

        Parameters:
        initial_spritesheet (list): The initial spritesheet containing animation frames.
        group (pygame.sprite.Group): The sprite group to which the entity belongs.
        rect_kwargs: Additional keyword arguments for setting the entity's rect.
        """
        self.animation_speed = ANIMATION_SPEED
        self.animation_index = 0
        self.spritesheet = initial_spritesheet
        self.last_frame_spritesheet = self.spritesheet
        image = self.spritesheet[self.animation_index]
        super().__init__(image, group, **rect_kwargs)

    def _handle_animation(self):
        """
        Update the animation frame based on the animation speed.
        """
        self.animation_index += self.animation_speed
        if (
            self.spritesheet != self.last_frame_spritesheet
            or self.animation_index >= len(self.spritesheet)
        ):
            self.animation_index = 0
        self.image = self.spritesheet[int(self.animation_index)]
        self.last_frame_spritesheet = self.spritesheet

    def _update_rect_and_mask(self):
        """
        Update the entity's rect and mask after changing the animation frame.
        """
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def change_animation_speed(self, new_animation_speed):
        """
        Change the animation speed of the entity.

        Parameters:
        new_animation_speed (float): The new animation speed.
        """
        self.animation_speed = new_animation_speed

    def update(self):
        """
        Update the animated entity.
        """
        self._handle_animation()
        self._update_rect_and_mask()


class AnimatedLivingEntity(LivingEntity):
    """
    Represents a living entity with animation capabilities in the game world.
    """

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
        """
        Initialize an animated living entity.

        Parameters:
        initial_spritesheet (list): The initial spritesheet containing animation frames.
        max_health (int): The maximum health value.
        current_health (int): The current health value.
        group (pygame.sprite.Group): The sprite group to which the entity belongs.
        health_bar_color (str): The color of the health bar.
        health_bar_pos (str): The position of the health bar relative to the entity.
        rect_kwargs: Additional keyword arguments for setting the entity's rect.
        """
        self.animation_speed = ANIMATION_SPEED
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
        """
        Update the animation frame based on the animation speed.
        """
        self.animation_index += ANIMATION_SPEED
        if (
            self.spritesheet != self.last_frame_spritesheet
            or self.animation_index >= len(self.spritesheet)
        ):
            self.animation_index = 0
        self.image = self.spritesheet[int(self.animation_index)]
        self.last_frame_spritesheet = self.spritesheet

    def _update_rect_and_mask(self):
        """
        Update the entity's rect and mask after changing the animation frame.
        """
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def change_animation_speed(self, new_animation_speed):
        """
        Change the animation speed of the entity.

        Parameters:
        new_animation_speed (float): The new animation speed.
        """
        self.animation_speed = new_animation_speed

    def update(self):
        """
        Update the animated living entity.
        """
        self._handle_animation()
        self._update_rect_and_mask()
