import pygame
import sprite


class Player(pygame.sprite.Sprite):
    X_SPEED = 5
    GRAVITY = 1
    JUMP_SPEED = 13
    MAX_JUMP_COUNT = 2
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, skin) -> None:
        super().__init__()
        self.rect = pygame.Rect(
            x, y, width * 2 // 4, height * 3 // 4
        )  # 2/4 and 3/4 are for hitbox
        self.width = width
        self.height = height
        self.x_vel = 0
        self.y_vel = 0

        self.jump_count = 0
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        self.direction = "right"
        self.animation_count = 0
        self.sprites = sprite.load_sprites("main-characters", skin, width, height, True)
        self.sprite = self.sprites["idle_" + self.direction][0]
        self.mask = pygame.mask.from_surface(self.sprite)  # For damage detection

    def move(self, objects) -> None:

        sign = lambda a: 1 if a > 0 else -1 if a < 0 else 0
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        player_shadow = self.rect.copy()

        # Handle Horizontal Collision
        for _ in range(abs(self.x_vel)):
            player_shadow.left += sign(self.x_vel)
            if len(Player._check_collision(player_shadow, objects)) > 0:
                player_shadow.left -= sign(self.x_vel)  # Undo movement
                if sign(self.x_vel) == 1:
                    self.collisions["right"] = True
                    self.stop()
                elif sign(self.x_vel) == -1:
                    self.collisions["left"] = True
                    self.stop()
                break

        # Handle Vertical Collision
        for _ in range(abs(self.y_vel)):
            player_shadow.top += sign(self.y_vel)
            if len(Player._check_collision(player_shadow, objects)) > 0:
                player_shadow.top -= sign(self.y_vel)  # Undo movement
                if sign(self.y_vel) == 1:
                    self.collisions["down"] = True
                    if self.y_vel == self.GRAVITY:  # Player is touching ground
                        self.y_vel = 0
                    else:
                        self.land()
                elif sign(self.y_vel) == -1:
                    self.collisions["up"] = True
                    self.hit_head()
                break

        # Update position
        self.rect.left = player_shadow.left
        self.rect.top = player_shadow.top

    def move_left(self) -> None:
        self.x_vel = -self.X_SPEED
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self) -> None:
        self.x_vel = self.X_SPEED
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def stop(self) -> None:
        if self.x_vel != 0:
            """self.animation_count = 0"""
            self.x_vel = 0

    def jump(self) -> None:
        if self.jump_count < self.MAX_JUMP_COUNT:
            self.jump_count += 1
            self.y_vel = -round(self.JUMP_SPEED * (1 + (1 - self.jump_count) * 0.2))
            self.animation_count = 0

    def land(self) -> None:
        self.y_vel = 0
        self.jump_count = 0
        self.animation_count = 0

    def hit_head(self) -> None:
        self.y_vel = -0.8 * self.y_vel
        self.animation_count = 0
        """ self.jump_count = 0 """

    @staticmethod
    def _check_collision(player_shadow, objects) -> tuple:
        collided_objects = []

        for object in objects:
            if player_shadow.colliderect(object.rect):
                collided_objects.append(object)

        return tuple(collided_objects)

    def loop(self, objets) -> None:
        self.y_vel = min(10, self.y_vel + self.GRAVITY)  # Gravity

        self.move(objets)
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
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window) -> None:
        pygame.draw.rect(window, (255, 0, 0), self.rect)
        window.blit(
            self.sprite,
            (self.rect.x - self.width * (1 / 4), self.rect.y - self.height * (1 / 4)),
        )  # Center the sprite on the hitbox
