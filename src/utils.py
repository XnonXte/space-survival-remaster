from os import path, listdir
import pygame


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
    background="black",
    **rect_kwargs,
):
    window = pygame.display.get_surface()
    text_surface = font.render(text, antialias, color, background)
    text_rect = text_surface.get_rect(**rect_kwargs)
    window.blit(text_surface, text_rect)


def render_text_with_outline(
    font,
    text,
    color=(255, 255, 255),
    outline_color=(0, 0, 0),
    outline_thickness=3,
    **rectkwargs,
):
    window = pygame.display.get_surface()
    outline_surface = font.render(text, True, outline_color).convert_alpha()
    outline_size = outline_surface.get_size()
    text_surface = pygame.Surface(
        (
            outline_size[0] + outline_thickness * 2,
            outline_size[1] + outline_thickness * 2,
        ),
        pygame.SRCALPHA,
    )
    text_rect = text_surface.get_rect()
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                text_surface.blit(
                    outline_surface, (dx + outline_thickness, dy + outline_thickness)
                )
    inner_text = font.render(text, True, color).convert_alpha()
    text_surface.blit(inner_text, inner_text.get_rect(center=text_rect.center))
    text_rect = text_surface.get_rect(**rectkwargs)
    window.blit(text_surface, text_rect)
