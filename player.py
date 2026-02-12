import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot




class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.power = 1
        self.normal_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.power_cooldown_timer = 0
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)
        self.power_cooldown_timer = max(0, self.power_cooldown_timer - dt)
        
        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        super().update(dt)
    
    def move(self, dt):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        # Use reduced cooldown if power cooldown is active
        cooldown = 0.05 if self.power_cooldown_timer > 0 else self.normal_cooldown
        
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = cooldown
        for i in range(self.power):
            forward = pygame.Vector2(0, 1).rotate(random.uniform(-10, 10) + self.rotation)
            shot = Shot(self.position.x + forward.x * self.radius, self.position.y + forward.y * self.radius, SHOT_RADIUS)
            shot.velocity = forward * PLAYER_SHOOT_SPEED
    
    def power_up(self):
        self.power += 1
    
    def activate_power_cooldown(self):
        self.power_cooldown_timer = 3
        