import pygame
from os import path, listdir


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
