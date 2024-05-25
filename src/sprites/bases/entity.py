import pygame
from .health_bar import HealthBar


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, group, **rect_kwargs):
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        super().__init__(group)


class LivingEntity(Entity):
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
        super().__init__(image, group, **rect_kwargs)
        self.health_bar = HealthBar(
            self, max_health, current_health, group, health_bar_color, health_bar_pos
        )

    def update_health(self, change_amount):
        self.health_bar.current_health += change_amount
        if self.health_bar.current_health <= 0:
            self.health_bar.current_health = 0
        if self.health_bar.current_health >= self.health_bar.max_health:
            self.health_bar.current_health = self.health_bar.max_health

    def update(self):
        super().update()
