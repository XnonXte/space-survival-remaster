from os import path
from sprites.bases import animated_entity
from utils import load_spritesheet


class Background(animated_entity.AnimatedEntity):
    BACKGROUND_SPRITESHEET = load_spritesheet(
        path.join("src", "assets", "graphics", "background")
    )

    def __init__(self, group):
        super().__init__(self.BACKGROUND_SPRITESHEET, group, topleft=(0, 0))

    def update(self):
        super().update()
