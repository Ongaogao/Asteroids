import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, ASTEROID_SPAWN_RATE_SECONDS=ASTEROID_SPAWN_RATE_SECONDS, ASTEROID_KINDS=ASTEROID_KINDS):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.ASTEROID_SPAWN_RATE_SECONDS= ASTEROID_SPAWN_RATE_SECONDS
        self.ASTEROID_KINDS = ASTEROID_KINDS

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        self.ASTEROID_SPAWN_RATE_SECONDS -= 0.01 * dt # Gradually increase spawn rate
        if self.ASTEROID_SPAWN_RATE_SECONDS < 0.5:
            self.ASTEROID_KINDS += 1 # Gradually increase asteroid variety
            self.ASTEROID_SPAWN_RATE_SECONDS = 1 - (self.ASTEROID_KINDS * 0.05) # Gradually decrease spawn rate
            if self.ASTEROID_SPAWN_RATE_SECONDS < 0.2:
                self.ASTEROID_SPAWN_RATE_SECONDS = 0.2 # Set a minimum spawn rate
        if self.spawn_timer > self.ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100) *(1 + 0.1 * self.ASTEROID_KINDS) # Gradually increase asteroid speed
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, self.ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)