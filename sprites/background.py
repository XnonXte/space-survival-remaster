from . import base
from os import path
from utils import load_spritesheet


class Background(base.AnimatedEntity):
    BACKGROUND_SPRITESHEET = load_spritesheet(
        path.join("assets", "graphics", "background")
    )

    def __init__(self, group):
        super().__init__(self.BACKGROUND_SPRITESHEET, group, topleft=(0, 0))

    def update(self):
        super().update()
