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
SCROLL_AREAR_WIDTH = 120
FPS = 60
BLOCKS_SIZE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_background(window, color) -> None:
    bg_image = pygame.image.load(join("assets", "backgrounds", color))
    _, _, width, height = bg_image.get_rect()

    for x in range(0, WIDTH, width):  # Fill screen with background tiles
        for y in range(0, HEIGHT, height):
            window.blit(bg_image, (x, y))


""" def draw_tiles(window, pos_list, image) -> None:
    for pos in pos_list:
        window.blit(image, pos) """


def draw_blocks(window, offset_x, blocks) -> None:
    for block in blocks:
        block.draw(window, offset_x)


keys_two_directions = False  # If player is pressing two directions at same time
keys_jumping_before = False  # If player is pressing jump key


def handle_keys(player) -> None:
    keys = pygame.key.get_pressed()
    global keys_two_directions, keys_jumping_before

    # X Movement
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

    # Y Movement
    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        if not keys_jumping_before:
            keys_jumping_before = True
            player.jump()
    else:
        keys_jumping_before = False


def main(window) -> None:
    clock = pygame.time.Clock()
    player = Player(0, 0, 2 * BLOCKS_SIZE, 2 * BLOCKS_SIZE, "mask-dude")
    blocks = [Block(i * BLOCKS_SIZE, 300, BLOCKS_SIZE) for i in range(50)]
    blocks.append(Block(BLOCKS_SIZE, 300 - BLOCKS_SIZE, BLOCKS_SIZE))

    offset_x = 0
    max_offset = 500  # Max offset of level

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Background
        draw_background(window, "green.png")

        # Blocks
        draw_blocks(window, offset_x, blocks)

        # Player
        handle_keys(player)
        player.loop(blocks)
        player.draw(window, offset_x)
        pygame.display.update()

        if (
            (player.rect.right - offset_x >= WIDTH - SCROLL_AREAR_WIDTH)
            and player.x_vel > 0
        ) or ((player.rect.left - offset_x <= SCROLL_AREAR_WIDTH) and player.x_vel < 0):
            offset_x += player.x_vel
            offset_x = max(0, min(max_offset, offset_x))

    # Exit window
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
