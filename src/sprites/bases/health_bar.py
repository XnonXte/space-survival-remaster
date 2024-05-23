import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(
        self,
        parent_sprite,
        max_health,
        current_health,
        group,
        health_bar_color="green",
        health_bar_pos="bottom",
    ):
        self.parent_sprite = parent_sprite
        self.max_health = max_health
        self.current_health = current_health
        self.health_bar_color = health_bar_color
        self.health_bar_pos = health_bar_pos
        self.health_bar_width = self.parent_sprite.rect.width
        self.health_bar_height = self.health_bar_width // 10
        self.image = pygame.Surface((self.health_bar_width, self.health_bar_height))

        # Determining which side should the health-bar take place.
        match self.health_bar_pos:
            case "bottom":
                self.rect = self.image.get_rect(
                    midtop=self.parent_sprite.rect.midbottom
                )
            case "top":
                self.rect = self.image.get_rect(
                    midbottom=self.parent_sprite.rect.midtop
                )
        super().__init__(group)

    def _update_health_bar(self):
        health_ratio = self.current_health / self.max_health
        fill_width = int(self.health_bar_width * health_ratio)
        self.image.fill("red")
        if fill_width > 0:
            pygame.draw.rect(
                self.image,
                self.health_bar_color,
                (0, 0, fill_width, self.health_bar_height),
            )

    def _update_health_bar_cord(self):
        match self.health_bar_pos:
            case "bottom":
                self.rect.midtop = self.parent_sprite.rect.midbottom
            case "top":
                self.rect.midbottom = self.parent_sprite.rect.midtop
            case _:
                raise Exception("Invalid health bar position!")

    def update(self):
        self._update_health_bar()
        self._update_health_bar_cord()
