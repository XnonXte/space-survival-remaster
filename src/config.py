from os import path
import pygame

# Inits.
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Important.
FPS = 75
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
ANIMATION_SPEED = 0.1
WINDOW_CAPTION = "Spaceships Remaster"

# Set display mode and caption.
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)

# Sizes.
PLAYER_SIZE = (64, 64)
ENEMY_SIZE = (64, 64)
DROP_SIZE = (64, 64)

# Player properties.
PLAYER_VEL = 3
PLAYER_BULLET_VEL = 6
PLAYER_BULLET_DAMAGE = 1
PLAYER_MAX_HEALTH = 5
PLAYER_MAX_SHIELD = 3
PLAYER_INVISIBILITY_ENEMY_COLLISION_COUNTDOWN = FPS * 4  # Essentially 4 seconds.
PLAYER_INVISIBILITY_HIT_COUNTDOWN = FPS * 2

# Enemy properties.
ENEMY_TYPES = ["black", "blue", "green", "red", "red_longwing"]
ENEMY_VEL = 1
ENEMY_BULLET_VEL = 3
ENEMY_BULLET_DAMAGE = 1
ENEMY_COLLISION_DAMAGE = 2
ENEMY_MAX_HEALTH = 3
ENEMY_BULLET_COOLDOWN = 4000

# Events.
ENEMY_PASSING_EVENT = pygame.USEREVENT + 1
ENEMY_KILLED_EVENT = pygame.USEREVENT + 2
GAME_OVER_EVENT = pygame.USEREVENT + 3

# Drop properties.
DROP_TIMEOUT = 4000
DROP_TYPE = ["heart", "shield"]
DROP_CHANCE = 10  # 10% drop change.

# Sfx.
ENEMY_GUN_SHOT_SFX = pygame.mixer.Sound(
    path.join("src", "assets", "sfx", "enemy_gun_shot.wav")
)
ENERGY_ORB_SFX = pygame.mixer.Sound(path.join("src", "assets", "sfx", "energy_orb.wav"))
EXPLODE_SFX = pygame.mixer.Sound(path.join("src", "assets", "sfx", "explode.wav"))
HEART_DROP_SFX = pygame.mixer.Sound(path.join("src", "assets", "sfx", "heart_drop.wav"))
HIT_MARK_SFX = pygame.mixer.Sound(path.join("src", "assets", "sfx", "hit_mark.wav"))
PLAYER_GUN_SHOT_SFX = pygame.mixer.Sound(
    path.join("src", "assets", "sfx", "player_gun_shot.wav")
)
SHIELD_DROP_SFX = pygame.mixer.Sound(
    path.join("src", "assets", "sfx", "shield_drop.wav")
)


# Flash properties.
FLASH_STEP_FRAME = FPS // 10
ALPHA_MAX = 255
ALPHA_TRANSPARENT = 32

# Fonts.
FONT_SIZE = 16
DOGICA_FONT = pygame.font.Font(
    path.join("src", "assets", "fonts", "dogica.ttf"), FONT_SIZE
)

# Wave properties.
PLAYER_VEL_INCREMENT = 1
PLAYER_FIRE_ANIMATION_SPEED_INCREMENT = 0.1
ENEMY_VEL_INCREMENT = 1
ENEMY_FIRE_ANIMATION_SPEED_INCREMENT = 0.05
WAVE_1_ENEMY_COOLDOWN = 4.0  # Seconds.
WAVE_2_ENEMY_COOLDOWN = 3.0
WAVE_3_ENEMY_COOLDOWN = 2.0
WAVE_4_ENEMY_COOLDOWN = 1.0
WAVE_5_ENEMY_COOLDOWN = 0.5  # Endless after wave 5.
WAVE_CHANGE_TIME = 60  # Seconds.
