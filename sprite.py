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
        for x in range(0, sprite_sheet.get_width(), 32):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            rect = pygame.Rect(x, 0, 32, 32)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface, (width, height)))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip_sprites(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def load_blocks(size, skin="grass"):
    path = join("assets", "terrain", "terrain.png")
    image = pygame.image.load(path).convert_alpha()

    all_sprites = {}
    skink_names = {
        "stone": (0, 0),
        "wood": (0, 1),
        "leaves": (0, 2),
        "grass": (1, 0),
        "desert": (1, 1),
        "purple-grass": (1, 2),
        "bricks": (3, 1),
    }
    sprites_names = [
        [
            "top-left",
            "top",
            "top-right",
            "inside-top-left",
            "inside-top-right",
        ],
        [
            "left",
            "center",
            "right",
            "inside-bottom-left",
            "inside-bottom-right",
        ],
        [
            "bottom-left",
            "bottom",
            "bottom-right",
        ],
    ]

    x_skin = skink_names[skin][0] * (16 * 6)
    if skin == "bricks":
        x_skin -= 16
    y_skin = skink_names[skin][1] * (16 * 4)

    for y in range(3):
        for x in range(5):
            if y == 2 and x > 2:
                break

            surface = pygame.Surface(
                (16, 16), pygame.SRCALPHA, 32
            )  # Each sprite is 16x16 in image

            rect = pygame.Rect(x_skin + x * 16, y_skin + y * 16, size, size)
            surface.blit(image, (0, 0), rect)
            all_sprites[sprites_names[y][x]] = pygame.transform.scale(
                surface, (size, size)
            )

    return all_sprites
