import pygame
from .health_bar import HealthBar


class Entity(pygame.sprite.Sprite):
    """
    Represents a basic entity in the game world.
    """

    def __init__(self, image, group, **rect_kwargs):
        """
        Initialize an entity.

        Parameters:
        image (pygame.Surface): The image representing the entity.
        group (pygame.sprite.Group): The sprite group to which the entity belongs.
        rect_kwargs: Additional keyword arguments for setting the entity's rect.
        """
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        super().__init__(group)


class LivingEntity(Entity):
    """
    Represents a living entity in the game world with health.
    """

    def __init__(
        self,
        max_health,
        current_health,
        image,
        group,
        health_bar_color,
        health_bar_pos,
        **rect_kwargs,
    ):
        """
        Initialize a living entity.

        Parameters:
        max_health (int): The maximum health value.
        current_health (int): The current health value.
        image (pygame.Surface): The image representing the entity.
        group (pygame.sprite.Group): The sprite group to which the entity belongs.
        health_bar_color (str): The color of the health bar.
        health_bar_pos (str): The position of the health bar relative to the entity.
        rect_kwargs: Additional keyword arguments for setting the entity's rect.
        """
        super().__init__(image, group, **rect_kwargs)
        self.health_bar = HealthBar(
            self, max_health, current_health, group, health_bar_color, health_bar_pos
        )

    def update_health(self, change_amount):
        """
        Update the current health of the entity.

        Parameters:
        change_amount (int): The amount by which the health should be changed.
        """
        self.health_bar.current_health += change_amount
        if self.health_bar.current_health <= 0:
            self.health_bar.current_health = 0
        if self.health_bar.current_health >= self.health_bar.max_health:
            self.health_bar.current_health = self.health_bar.max_health

    def update(self):
        """
        Update the living entity.
        """
        super().update()
