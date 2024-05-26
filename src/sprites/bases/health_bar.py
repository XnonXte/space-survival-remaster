import pygame


class HealthBar(pygame.sprite.Sprite):
    """
    Represents a health bar for a sprite.
    """

    def __init__(
        self,
        parent_sprite,
        max_health,
        current_health,
        group,
        health_bar_color="green",
        health_bar_pos="bottom",
    ):
        """
        Initialize a health bar.

        Parameters:
        parent_sprite (pygame.sprite.Sprite): The sprite the health bar belongs to.
        max_health (int): The maximum health value.
        current_health (int): The current health value.
        group (pygame.sprite.Group): The sprite group to which the health bar belongs.
        health_bar_color (str): The color of the health bar.
        health_bar_pos (str): The position of the health bar relative to the parent sprite.
        """
        self.parent_sprite = parent_sprite
        self.max_health = max_health
        self.current_health = current_health
        self.health_bar_color = health_bar_color
        self.health_bar_pos = health_bar_pos
        self.health_bar_width = self.parent_sprite.rect.width
        self.health_bar_height = self.health_bar_width // 10
        self.image = pygame.Surface((self.health_bar_width, self.health_bar_height))

        # Set the initial position of the health bar based on the specified position.
        if self.health_bar_pos == "bottom":
            self.rect = self.image.get_rect(midtop=self.parent_sprite.rect.midbottom)
        elif self.health_bar_pos == "top":
            self.rect = self.image.get_rect(midbottom=self.parent_sprite.rect.midtop)
        else:
            raise ValueError("Invalid health bar position!")

        super().__init__(group)

    def _update_health_bar(self):
        """
        Update the appearance of the health bar based on the current health.
        """
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
        """
        Update the position of the health bar relative to the parent sprite.
        """
        if self.health_bar_pos == "bottom":
            self.rect.midtop = self.parent_sprite.rect.midbottom
        elif self.health_bar_pos == "top":
            self.rect.midbottom = self.parent_sprite.rect.midtop

    def update(self):
        """
        Update the health bar.
        """
        self._update_health_bar()
        self._update_health_bar_cord()
