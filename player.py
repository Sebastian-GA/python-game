import pygame


class Player(pygame.sprite.Sprite):
    PLAYER_SPEED = 5
    GRAVITY = 1

    def __init__(self, x, y, width, height) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False

        self.direction = "left"
        self.animation_count = 0

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
        self.x_vel = 0

    def loop(self, fps) -> None:
        if not self.on_ground:
            self.y_vel = min(10, self.y_vel + self.GRAVITY)

        self.move(self.x_vel, self.y_vel)

    def draw(self, window) -> None:
        pygame.draw.rect(window, (255, 0, 0), self.rect)
