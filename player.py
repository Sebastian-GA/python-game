import pygame
import sprite


class Player(pygame.sprite.Sprite):
    PLAYER_SPEED = 5
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, skin) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = True
        self.mask = None

        self.direction = "right"
        self.animation_count = 0
        self.sprites = sprite.load_sprites("main-characters", skin, width, height, True)
        self.sprite = self.sprites["idle_" + self.direction][0]

    def move(self, dx, dy) -> None:
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self) -> None:
        self.x_vel = -self.PLAYER_SPEED
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self) -> None:
        self.x_vel = self.PLAYER_SPEED
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def stop(self) -> None:
        if self.x_vel != 0:
            self.animation_count = 0
            self.x_vel = 0

    def loop(self, fps) -> None:
        # Update Position
        if not self.on_ground:
            self.y_vel = min(10, self.y_vel + self.GRAVITY)

        self.move(self.x_vel, self.y_vel)
        self.update_sprite()

    def update_sprite(self) -> None:
        if self.y_vel < 0:
            status = "jump"
        elif self.y_vel > 0:
            status = "fall"
        else:  # On Ground
            if self.x_vel != 0:
                status = "run"
            else:
                status = "idle"

        sprite_id = f"{status}_{self.direction}"
        self.animation_count = (self.animation_count + 1) % (
            len(self.sprites[sprite_id]) * self.ANIMATION_DELAY
        )
        sprite_index = self.animation_count // self.ANIMATION_DELAY
        self.sprite = self.sprites[sprite_id][sprite_index]
        self.update()

    def update(self) -> None:
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window) -> None:
        """pygame.draw.rect(window, (255, 0, 0), self.rect)"""
        window.blit(self.sprite, (self.rect.x, self.rect.y))
