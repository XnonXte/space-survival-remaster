import pygame
from .animated_entity import AnimatedEntity, AnimatedLivingEntity
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class MoveableAnimatedEntity(AnimatedEntity):
    """
    Represents an animated entity that can move.
    """

    def __init__(self, vel, initial_spritesheet, group, **rect_kwargs):
        """
        Initialize a moveable animated entity.

        Parameters:
        vel (int): The velocity of the entity.
        initial_spritesheet (list): The initial spritesheet for the entity.
        group (pygame.sprite.Group): The group this sprite will be added to.
        **rect_kwargs: Additional arguments for the sprite's rectangle.
        """
        self.vel = vel
        self.direction = pygame.math.Vector2()
        super().__init__(initial_spritesheet, group, **rect_kwargs)

    def _handle_y_movement(self, keys):
        """
        Handle vertical movement based on key presses.
        """
        if keys[pygame.K_w] and self.rect.top > 0:
            self.direction.y = -1
        elif keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def _handle_x_movement(self, keys):
        """
        Handle horizontal movement based on key presses.
        """
        if keys[pygame.K_a] and self.rect.left > 0:
            self.direction.x = -1
        elif keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def _normalize_vector(self):
        """
        Normalize the movement vector to prevent faster diagonal movement.
        """
        if self.direction.length() > 0:
            self.direction.normalize_ip()

    def _handle_movement(self):
        """
        Handle overall movement by processing input and applying movement.
        """
        keys = pygame.key.get_pressed()
        self._handle_y_movement(keys)
        self._handle_x_movement(keys)
        self._normalize_vector()
        self._apply_movement()

    def _apply_movement(self):
        """
        Apply the movement to the entity.
        """
        self.rect.center += self.direction * self.vel

    def change_vel(self, new_vel):
        """
        Change the velocity of the entity.

        Parameters:
        new_vel (int): The new velocity.
        """
        self.vel = new_vel

    def update(self):
        """
        Update the entity's state.
        """
        super().update()
        self._handle_movement()


class MoveableAnimatedLivingEntity(AnimatedLivingEntity):
    """
    Represents an animated living entity that can move.
    """

    def __init__(
        self,
        vel,
        initial_spritesheet,
        max_health,
        current_health,
        group,
        health_bar_color,
        health_bar_pos,
        **rect_kwargs,
    ):
        """
        Initialize a moveable animated living entity.

        Parameters:
        vel (int): The velocity of the entity.
        initial_spritesheet (list): The initial spritesheet for the entity.
        max_health (int): The maximum health of the entity.
        current_health (int): The current health of the entity.
        group (pygame.sprite.Group): The group this sprite will be added to.
        health_bar_color (str): The color of the health bar.
        health_bar_pos (str): The position of the health bar.
        **rect_kwargs: Additional arguments for the sprite's rectangle.
        """
        self.vel = vel
        self.direction = pygame.math.Vector2()
        super().__init__(
            initial_spritesheet,
            max_health,
            current_health,
            group,
            health_bar_color,
            health_bar_pos,
            **rect_kwargs,
        )

    def _handle_y_movement(self, keys):
        """
        Handle vertical movement based on key presses.
        """
        if keys[pygame.K_w] and self.rect.top > 0:
            self.direction.y = -1
        elif keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def _handle_x_movement(self, keys):
        """
        Handle horizontal movement based on key presses.
        """
        if keys[pygame.K_a] and self.rect.left > 0:
            self.direction.x = -1
        elif keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def _normalize_vector(self):
        """
        Normalize the movement vector to prevent faster diagonal movement.
        """
        if self.direction.length() > 0:
            self.direction.normalize_ip()

    def _handle_movement(self):
        """
        Handle overall movement by processing input and applying movement.
        """
        keys = pygame.key.get_pressed()
        self._handle_y_movement(keys)
        self._handle_x_movement(keys)
        self._normalize_vector()
        self._apply_movement()

    def _apply_movement(self):
        """
        Apply the movement to the entity.
        """
        self.rect.center += self.direction * self.vel

    def change_vel(self, new_vel):
        """
        Change the velocity of the entity.

        Parameters:
        new_vel (int): The new velocity.
        """
        self.vel = new_vel

    def update(self):
        """
        Update the entity's state.
        """
        super().update()
        self._handle_movement()
