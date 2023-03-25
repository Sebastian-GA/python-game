import pygame
from os import listdir
from os.path import isfile, join


def flip_sprites(sprites):
    sprites_flipped = []
    for sprite in sprites.copy():
        sprites_flipped.append(pygame.transform.flip(sprite, True, False))
    return sprites_flipped


def load_sprites(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for x in range(0, sprite_sheet.get_width(), width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(x, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip_sprites(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites
