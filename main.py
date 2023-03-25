import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

from player import Player
from object import Block  # , Coin, Enemy, Flag, Flagpole, Goal, Lava, Water

pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 800, 600
FPS = 60
BLOCKS_SIZE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_background(window, color) -> None:
    bg_image = pygame.image.load(join("assets", "Backgrounds", color))
    _, _, width, height = bg_image.get_rect()

    for x in range(0, WIDTH, width):  # Fill screen with background tiles
        for y in range(0, HEIGHT, height):
            window.blit(bg_image, (x, y))


def draw_tiles(window, pos_list, image) -> None:
    for pos in pos_list:
        window.blit(image, pos)


keys_two_directions = False  # If player is pressing two directions at same time


def handle_keys(player) -> None:
    keys = pygame.key.get_pressed()
    global keys_two_directions

    # Player is pressing two directions at same time
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (
        keys[pygame.K_RIGHT] or keys[pygame.K_d]
    ):
        if not keys_two_directions:  # If player was not pressing two directions before
            keys_two_directions = True  # Set two_directions flag to True
            # And move to opposite direction of last direction
            last_direction = player.direction
            if last_direction == "left":
                player.move_right()
            else:
                player.move_left()
    else:
        # Player is pressing only one direction
        keys_two_directions = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Left
            player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Right
            player.move_right()
        else:
            player.stop()


def main(window) -> None:
    clock = pygame.time.Clock()
    player = Player(0, 0, 2 * BLOCKS_SIZE, 2 * BLOCKS_SIZE, "Ninja Frog")
    block1 = Block(0, 0)
    block2 = Block(0, BLOCKS_SIZE)
    block3 = Block(0, 2 * BLOCKS_SIZE)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Background
        draw_background(window, "Green.png")

        # Blocks
        block1.draw(window)
        block2.draw(window)
        block3.draw(window)

        # Player
        handle_keys(player)
        player.loop(FPS)
        player.draw(window)

        pygame.display.update()

    # Exit window
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
