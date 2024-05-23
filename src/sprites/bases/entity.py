import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, group, **rect_kwargs):
        self.image = image
        self.rect = self.image.get_rect(**rect_kwargs)
        super().__init__(group)
