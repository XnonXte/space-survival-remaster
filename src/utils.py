import json
from os import path, listdir
import pygame
from config import HISTORY_FILE_PATH


def rotate_spritesheet(spritesheet, angle):
    rotated_spritesheet = []
    for sprite in spritesheet:
        rotated_spritesheet.append(pygame.transform.rotate(sprite, angle))
    return rotated_spritesheet


def load_spritesheet(spritesheet_dir):
    sprites = [
        pygame.image.load(path.join(spritesheet_dir, sprite)).convert_alpha()
        for sprite in listdir(spritesheet_dir)
        if path.isfile(path.join(spritesheet_dir, sprite))
    ]
    return sprites


def render_text(
    text,
    font,
    antialias=True,
    color="white",
    **rect_kwargs,
):
    window = pygame.display.get_surface()
    text_surface = font.render(text, antialias, color)
    text_rect = text_surface.get_rect(**rect_kwargs)
    window.blit(text_surface, text_rect)


def read_history():
    with open(HISTORY_FILE_PATH, "r") as file:
        return json.load(file)


def save_history(new_history):
    with open(HISTORY_FILE_PATH, "w") as file:
        file.write(json.dumps(new_history))
