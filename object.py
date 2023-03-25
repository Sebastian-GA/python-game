import pygame
import sprite


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.sprite)

        self.width = width
        self.height = height
        self.name = name

    def draw(self, window) -> None:
        window.blit(self.sprite, (self.rect.x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size=32) -> None:
        super().__init__(x, y, size, size)
        self.sprites = sprite.load_blocks(size)
        self.update_sprite()

    def update_sprite(self, name="top") -> None:
        self.sprite = self.sprites[name]
        self.mask = pygame.mask.from_surface(self.sprite)
