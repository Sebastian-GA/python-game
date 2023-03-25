import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

from player import Player

pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 800, 600
FPS = 60

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


def main(window) -> None:
    clock = pygame.time.Clock()
    player = Player(0, 0, 50, 50)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Background
        window.fill((255, 255, 255))
        draw_background(window, "Green.png")

        # Player
        player.loop(FPS)
        player.draw(window)

        pygame.display.update()

    # Exit window
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
