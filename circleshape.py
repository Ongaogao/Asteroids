import pygame
from constants import LINE_WIDTH,SCREEN_WIDTH, SCREEN_HEIGHT


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        # This keeps x within the bounds of 0 and SCREEN_WIDTH
        shifted_x = self.position.x + self.radius
        shifted_y = self.position.y + self.radius
        self.position.x = shifted_x % (SCREEN_WIDTH + 2 * self.radius) - self.radius
        self.position.y = shifted_y % (SCREEN_HEIGHT + 2 * self.radius) - self.radius
    
    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        if distance < self.radius + other.radius:
            return True
        return False