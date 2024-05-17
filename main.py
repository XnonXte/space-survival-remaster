# TODO: Finalize player movement. (DONE)
# TODO: Add background with animation. (DONE)
# TODO: Create the enemy logic. (DONE)
# TODO: Create the bullet logic (both player and enemy). (DONE)
# TODO: Create health and shield system.
# TODO: Implement a healthbar system which follows a sprite?
# TODO: Implement a healthbar indicator on the top left, and shield indicator on the top right.
# TODO: Create a simple main menu? (https://youtu.be/2iyx8_elcYg?si=RjqQtYt5eEmDjyrb)
# TODO: Store score in a JSON file.
# TODO: Maybe at this point get a history system where you can see your past play?
# TODO: Release...

import pygame
from config import window, clock
from sprites import *
from constants import FPS


class Game:
    def draw_and_update_groups(self, *groups):
        for group in groups:
            group.draw(window)
            group.update()

    def run(self):
        background_group = pygame.sprite.GroupSingle()
        player_group = pygame.sprite.GroupSingle()
        enemy_group = pygame.sprite.Group()
        player_bullet_group = pygame.sprite.Group()
        enemy_bullet_group = pygame.sprite.Group()
        Background(background_group)
        player_sprite = Player(player_bullet_group, enemy_group, player_group)
        Enemy((0, 0), enemy_bullet_group, player_sprite, "red", enemy_group)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player_sprite.fire()

            window.fill("black")
            self.draw_and_update_groups(
                background_group,
                player_group,
                enemy_group,
                player_bullet_group,
                enemy_bullet_group,
            )
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
        quit(0)


if __name__ == "__main__":
    game = Game()
    game.run()
