import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_CAPTION)
