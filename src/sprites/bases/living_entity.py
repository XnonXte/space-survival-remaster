from .entity import Entity
from .health_bar import HealthBar


class LivingEntity(Entity):
    def __init__(
        self,
        max_health,
        current_health,
        image,
        group,
        dying_callback,
        health_bar_color,
        health_bar_pos,
        **rect_kwargs,
    ):
        super().__init__(image, group, **rect_kwargs)
        self.health_bar = HealthBar(
            self, max_health, current_health, group, health_bar_color, health_bar_pos
        )
        self.dying_callback = dying_callback

    def update_health(self, change_amount):
        self.health_bar.current_health += change_amount
        if self.health_bar.current_health <= 0:
            self.dying_callback()
            self.health_bar.kill()
            self.kill()
        if self.health_bar.current_health >= self.health_bar.max_health:
            self.health_bar.current_health = self.health_bar.max_health

    def update(self):
        super().update()
