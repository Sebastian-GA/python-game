import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def set_background(window, color):
    bg_image = pygame.image.load(join("assets", "Backgrounds", color))
    _, _, width, height = bg_image.get_rect()

    for x in range(0, WIDTH, width):  # Fill screen with background tiles
        for y in range(0, HEIGHT, height):
            window.blit(bg_image, (x, y))

    pygame.display.update()


def draw(window, pos_list, image):
    for pos in pos_list:
        window.blit(image, pos)

    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Background
        window.fill((255, 255, 255))
        set_background(window, "Green.png")

        pygame.display.update()

    # Exit window
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
